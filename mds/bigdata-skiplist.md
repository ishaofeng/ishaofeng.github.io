title: 大数据算法之SkipList
tags: 读书笔记
date: 2014-10-30
***
###1.前言
最早在了解LevelDB的时候指导SkipList,之前在阅读Redis代码的时候了解到Redis中的zset的实现使用了SkipList，今天看书把SkipList自己实现一下并且查了一下资料了解一下SkipList的使用。

###2.特点
SkipList是一种可以替代平衡二叉搜索树的数据结构，二叉树不需要强制平衡，使用随机生成树在一定概率上保证数据的分布平衡，其插入，删除和查找的时间复杂度为*O(log(N))*.

**优点：**

> * 在SkipList上的插入或者删除仅仅影响和它相邻的节点，只产生局部影响，而平衡二叉树可能存在大量节点参与的再平衡
> * 因为操作的局部影响的特点，SkipList能够支持更高的并发操作，小粒度的锁能够保证多个读者写者同时对数据结构进行操作
> * Cache友好，在并发环境下如果在节点增删只有很少量节点发生改变因而多核的缓存不需要更新，从而对Cache友好
> * 并发操作下使用 Hand-over-hand locking保证不产生死锁，所有操作要进行小范围的加所的时候都是从前向后加

###3.实现
下述代码是我使用C写的一个实现SkipList结构中使用的一个SkipListNode作为header,从而简化在没有节点时的操作

    #include "cbase.h"

    /*
     * SkipList数据结构实现
     */
    
    #define MAX_LEVEL 8


    typedef struct SkipListNode
    {
      int key;
    void *value;
    int level;

    struct SkipListNode *forward[MAX_LEVEL];
    } SkipListNode;

    typedef struct SkipList
    {
        int level;  //当前最高层
        SkipListNode header;
    } SkipList;

    //释放节点值
    void freeValue(void *value)
    {
        if (value != NULL)
        {
            free(value);
        }
    }

    //创建SkipList
    SkipList *createSkipList()
    {
        SkipList *list = (SkipList *)malloc(sizeof(SkipList));
        if (NULL == list)
        {
            return NULL;
        }

        list->level = 0;
        memset(list->header.forward, 0, sizeof(SkipListNode *) * MAX_LEVEL);

        return list;
    }

    //释放SkipListNode
    void destroySkipListNode(SkipListNode *node)
    {
        if (NULL == node)
        {
            return ;
        }

        freeValue(node->value);
        free(node);
    }

    //释放SkipList
    void destroySkipList(SkipList **list)
    {
        if (NULL == list)
        {
            return ;
        }

        SkipListNode *current  = &(*list)->header, *deleteNode;
        while (current->forward[0] != NULL)
        {
            deleteNode = current->forward[0];

            current->forward[0] = deleteNode->forward[0];

            destroySkipListNode(deleteNode);
        }

        free(*list);

        *list = NULL;
    }


    //创建SkipList节点
    SkipListNode *createSkipListNode(int key, void *value, int level)
    {
        SkipListNode *node = (SkipListNode *)malloc(sizeof(SkipListNode));
        if (NULL == node)
        {
            return NULL;
        }

        node->key = key;
        node->value = value;
        node->level = level;

        memset(node->forward, 0, sizeof(SkipListNode *) * MAX_LEVEL);

        return node;

    }
    //随机生成层次
    int randomLevel()
    {
        int level = 0;

        while (rand() * 1.0 / RAND_MAX > 0.5 && level < MAX_LEVEL)
        {
            ++level;
        }

        return level;
    }


    //插入元素
    SkipList *insertSkipList(SkipList *list, int key, void *value)
    {
        if (NULL == list)
        {
            return list;
        }

        SkipListNode *update[MAX_LEVEL];
        SkipListNode *current = &list->header;

        for (int i = list->level; i >= 0; --i)
        {
            while (current->forward[i] != NULL && current->forward[i]->key < key)
            {
                current = current->forward[i];
            }

            update[i] = current;
        }

        current = update[0]->forward[0];
        if (current != NULL && current->key == key) //插入的节点已经存在
        {
            freeValue(current->value);
            current->value = value;
        }
        else //插入新节点
        {
            //更新skiplist最高层次
            int level = randomLevel();
            if (level > list->level)
            {
                for (int i = list->level + 1; i <= level; ++i)
                {
                    update[i] = &list->header;
                }
                list->level = level;
            }

            SkipListNode *newnode = createSkipListNode(key, value, level);
            assert(newnode != NULL);

            //插入节点
            for (int i = 0; i <= level; ++i)
            {
                newnode->forward[i] = update[i]->forward[i];
                update[i]->forward[i] = newnode;
            }
        }
    }

    //搜索skiplist
    SkipListNode *searchSkipList(SkipList *list, int key)
    {
        if (NULL == list)
        {
            return NULL;
        }

        SkipListNode *current = &list->header;
        for (int i = list->level; i >= 0; --i)
        {
            while (current->forward[i] != NULL && current->forward[i]->key < key)
            {
                current = current->forward[i];
            }

            if (current->forward[i] != NULL && current->forward[i]->key == key)
            {
                return current->forward[i];
            }
        }

        return NULL;
    }

    //删除skiplist节点
    void deleteSkipList(SkipList *list, int key)
    {
        if (NULL == list)
        {
            return ;
        }

        SkipListNode *update[MAX_LEVEL];
        SkipListNode *current = &list->header;

        for (int i = list->level; i >= 0; --i)
        {
            while (current->forward[i] != NULL && current->forward[i]->key < key)
            {
                current = current->forward[i];
            }

            update[i] = current;
        }

        current = update[0]->forward[0];
        if (current != NULL && current->key == key) //找到要删除的节点
        {
            freeValue(current->value);

            for (int i = 0; i <= current->level; ++i)
            {
                update[i]->forward[i] = current->forward[i];
            }

            if (current->level == list->level && NULL == list->header.forward[list->level])
            {
                --list->level;
            }
        }
    }
    //辅助函数
    //打印skiplist
    void printSkipList(SkipList *list)
    {
        if (NULL == list)
        {
            return ;
        }

        SkipListNode *current = list->header.forward[0];
        printf("=======skiplist=======\n");
        while (current != NULL)
        {
            println("key: %d  level: %d", current->key, current->level);
            current = current->forward[0];
        }
    }

    int main()
    {
        srand(time(NULL));

        printf("插入\n");
        SkipList *list = createSkipList();
        insertSkipList(list, 10, NULL);
        insertSkipList(list, 1, NULL);
        insertSkipList(list, 12, NULL);
        insertSkipList(list, 7, NULL);
        insertSkipList(list, 9, NULL);
        insertSkipList(list, 3, NULL);
        insertSkipList(list, 28, NULL);
        insertSkipList(list, 29, NULL);
        insertSkipList(list, 11, NULL);
        insertSkipList(list, 30, NULL);
        insertSkipList(list, 27, NULL);

        printSkipList(list);

        printf("删除\n");
        deleteSkipList(list, 10);
        printSkipList(list);

        println("查找: %d", searchSkipList(list, 30)->key);

        return 0;
    }
***

[[1]Choose Concurrency-Friendly Data Structures](http://www.drdobbs.com/parallel/choose-concurrency-friendly-data-structu/208801371)



