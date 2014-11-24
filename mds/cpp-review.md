title: cppreview
tags: cpp
date: 2014-11-22
***
很久没有写纯粹的cpp代码，使用Qt都是Qt自身提供的一套库，周末把cpp标准库(包括cpp11新特性)学习了一下，记录了一些关键接口和用法，regex和random等章节有待完善
##1. IO类
**要点:**

* IO类不能进行拷贝或者赋值

**类型:**

* 面向终端 istream,ostream,iostream
* 面向文件 ifstream,ofstream,fstream
* 面向字符串 istringstream,ostringstream,stringstream

**接口相关状态:**

* strm::iostate设备无关表示一个流的状态
    * strm::badbit表示流损坏
    * strm::failbit表示IO操作失败
    * strm::eofbit表示文件结束
    * strm::goodbit表示流在非错误状态
* s.eof()文件是否结束
* s.fail() strm::badbit或者strm::failbit设置
* s.bad() strm::badbit设置
* s.good() 是否正常状态
* s.clear() 移除所有状态值
* s.clear(flag) 清楚特定状态值
* s.setstate(flags) 设置特定状态值
* s.rdstate() 读取当前状态值

```
unitbuf
当读cin和写cerr时cout的buffer将会被刷新, (tied)
cin.tie(&cout)
cin.tie(nullptr)

cout << unitbuf;
cout << nounitbuf;

程序崩溃buffer将不刷新
```

**文件的打开方式:**

* **in**读模式
* **out**写模式
* **app**在文件尾追加
* **ate**打开后立即到文件尾
* **trunc**截断文件
* **binary**二进制模式操作文件

```
getline(cin, str);

ostringstream os;
os << "hello";
os.str();
```

##2.顺序容器

* **vector**
    * 动态数组
    * 支持随机访问
    * 在末尾插入或者删除常量时间
    * 其它地方插入或者删除o(n)
* **deque**
    * 双端队列
    * 支持随机访问
    * 首尾支持快速的随即访问
* **list**
    * 双端链表
    * 支持双向顺序访问
    * 任意位置快速的插入和删除
* **forward_list**
    * 单链表
    * 支持单向访问
    * 任意快速的插入和删除
* **array**
    * 定长数组
    * 支持随机访问
    * 不能添加或者删除元素
* **string**
    * 特殊容器，与vector类似
    * 快速随机访问
    * 在末尾快速的插入和删除
除过array外所有容器都提供高效灵活的内存管理, 我们能够添加和删除元素，
增大或者缩小容器的大小

###2.1通用操作
**数据类型:**

* iterator 迭代器
* const_iterator 只读迭代器
* size_type 容器尺寸类型
* difference_type 两个迭代器的差值类型
* value_type 容器元素类型
* reference 元素引用类型
* const_reference 常量元素引用

**构造器:**

* `C c`默认构造函数
* `C c1(c2)`拷贝构造函数
* `C c(b, e)`拷贝b,e两个迭代器之间的元素
* `C c{a,b,c...}`列表初始化

**赋值和交换:**

* c1 = c2赋值
* c1 = {a,b,c...}
* a.swap(b)
* swap(a, b)

**大小:**

* c.size() 当前元素个数(forward_list没有元素个数)
* c.max_size() 最大元素个数
* c.empty()
* c.resize(n)/c.resize(n, t) 改变容器的大小, 如果大小小于当前大小
将会从尾部删除元素，如果大于当前大小则会增加元素，如果带t新增加的
元素的值为t, resize操作将使得迭代器失效，尤其对于连续内存的所有迭代
器将失效

容器中的元素必须有构造函数,如果没有构造函数那么应该带有初始化值

**forward_list特殊操作:**
* c.before_begin()
* c.insert_after(p, t)
* c.insert_after(p, n, t)
* c.insert_after(p, b, e)
* c.erase_after(p)
* c.erase_after(b, e)

**vector和string中的内存管理:**
* c.shrink_to_fit()请求减少capacity()到size()
* c.capacity()在重新分配内存之前c能容纳的元素个数
* c.reserve(n)预保留能够容纳n个元素的空间

###2.2tring额外的操作
* s(cp,n)字符数组n个字符
* s(s2, pos)从s2的pos开始的字符
* s(s2, pos, len)从s2的pos开始的len个字符
* s.substr(pos, n)子串
* s.insert(i, n, c)在字符串索引i处插入n个char
* s.erase(i, 5)从索引i处开始删除五个字符
* s.assign(cp, n)使用cp开始的n个字符替换s的内容
* s.append
* s.replace
***
* s.find(args)查找s中args第一次出现位置
* s.rfind(args)查找s中args最后一次出现位置
* s.find_first_of(args)查找args中的任意元素第一次出现
* s.find_last_of(args)查找args中的任意元素最后一次出现位置
* s.find_first_not_of(args)查找第一个不是args中任意元素的位置
* s.find_last_not_of(args)


**args:**
* `c, pos`
* `s2, pos`
* `cp, pos`
* `cp, pos, n`

搜索函数的返回值类型为string::size_type

`string::npos`表示搜索失败

***
* s.compare(args)

**args:**
* s2
* pos1,n1,s2
* pos1,n1,s2,pos2,n2
* cp
* pos1,n1,cp
* pos1,n1,cp,n2

***

* to_string(val)将数值类型转换为string
* stoi(s, p, b)
* stol(s, p, b)
* stoul(s, p, b)
* stoll(s, p, b)
* stoull(s, p, b)
* stof(s, p, b)
* stod(s, p, b)
* stold(s, p, b)

> 上述上述转换过程非法将抛出invalid_argument异常
> 如果转化的数值超过表示区域将抛出out_of_range


**注意:**
* 不要缓存end返回的迭代器，因为在使用过程中迭代器可能失效

###2.3容器适配器
适配器在库中是一种通用概念，包括容器，迭代器和函数适配器，
适配器的意义是使得一种东西表现的像另一种东西

* stack
* queue
* priority_queue

**通用操作和类型:**
* size_type
* value_type
* container_type
* a.empty()
* a.size()
* swap(a,b)
* a.swap(b)

*默认情况下stack和queue是使用deque容器实现,priority_queue是
使用vector容器实现, 使用下述方式能够自定义适配器所使用的容器:

    stack<string, vector<string> > str_stk;
    stack<string, vector<string>> str_stk2(svec)

##3.算法
一组通用算法能够应用到连续容器或者内建数组, 大部分算法定义在
algorithm头中，一部分数值相关的定义在numeric中


###3.2 Lambda表达式
**可调用的类型:**

* 函数
* 函数指针
* 函数对象(重载了函数调用操作符的类)
* lambda表达式

**lambda表达式**表示一个可调用的代码单元

* 匿名
* inline
* 有返回值
* 可以在一个函数内定义

**使用原型:**

    [capture list] (parameter list) -> return type  {function body}

    auto f = [] {reutrn 43;};
    cout << f() << endl;

    auto isShorter = [] (const string &a, const string &b) { return a < b; };
                        

* 如果不指定返回类型那么将使用代码块中返回的类型
* 如果没有指定返回类型并且代码快中只有一个return那么返回类型是void
* `capture list`表示要使用的外部本地变量
    
    vector<int> b{1, 2, 3, 4, 5};
    int a = 3;
    auto eq = [a](const int &b) {return a == b;};
    find_if(b.begin(), b.end(), eq);

**原理:**

当我们定义一个lambda, 编译器将生成一个匿名类，并且生成这个匿名类的对象
匿名类的数据成员就是`cpature list`中的数据，lambda的数据成员是在一个lambda对象
创建的时候初始化.

**lambda对象数据成员初始化方式:**
* [] 空list
* [names]使用逗号分割的本地变量
* [&]
* [=]
* [&,identifier_list]
* [=,reference_list]



###3.3 函数参数绑定
定义在头文件functionnal中

**使用原型:**

    auto newCallable = bind(callable, arg_list);

**arg_list:**参数列表中的是逗号分割的变量，其中可以使用`_n`表示
一个函数参数替代位置, n从１开始表示, `_n`本身定义在std::placeholders命名空间中

* 使用bind可以改变参数的顺序
* bind传入的本地参数默认是使用值传递, 如果需要传递引用的话使用
ref(arg)变量arg,那么传递的参数就是引用
* 静态应用传递使用cref(arg)

###3.4 RevisitingIterators
除过为容器定义的迭代器，标准库还在iterator头文件中定义了一些额外的迭代器

####3.4.1 **InsertIterator:**容器使用的迭代器，用来在容器中插入元素

* back_inserter创建一个使用push_back的插入迭代器
```
    vector<int> a{1, 2, 3, 4};
    vector<int> b;

    auto b = back_inserter(a);
    *b = val;
    //上述语句等价于
    //a.push_back(val);
```
* front_inserter创建一个使用push_front的插入迭代器
```
    vector<int> a{1, 2, 3, 4};
    vector<int> b;

    auto b = front_inserter(a);
    *b = val;
    //上述语句等价于
    //a.push_front(val);
```
* inserter创建一个使用insert的插入迭代器

    vector<int> a{1, 2, 3, 4};
    vector<int> b;

    auto b = front_inserter(a, a.begin());
    *b = val;
    //上述语句等价于
    //b = a.insert(b, val);
    //++b;


####3.4.2 **StreamIterator:**输入输出流使用迭代器,能够在关联的流中迭代
* istream_iterator
    * `istream_iterator<T> in(is)`in能够读取T类型数据从is流中
    * `istream_iterator<T> end`istream_iterator的结束
    * `in1 == in2`读取相同类型并且对应相同的流
    * `++in,in++`读取下一个值

* ostream_iterator
    * `ostream_iterator<T> out(os)`out能都写出T类型的值到os
    * `ostream_iterator<T> out(os, d)`out能写出T类型的值到os并写出d字符
    * `out = val`写出val到os

    
    istream_iterator<int> in_iter(cin);
    istream_iterator<int> eof;
    while (in_iter != eof)
    {
        vec.push_back(*in_iter++);
    }
    //上述等价于
    vector<int> vec(in_iter, eof);
    //等价于
    vector<int> vec;
    copy(vec.begin(), vec.end(), back_inserter(vec))
    //ostream
    ostream_iterator<int> out_iter(cout, " ");
    for (auto e : vec)
    {
        *out_iter++ = e;
    }
    cout << endl;
    //同上
    copy(vec.bein(), vec.end(), out_iter);
    cout << endl;

####3.4.3 **ReverseIterator:**反向迭代器
####3.4.4 **MoveIterator:**

####3.5 list专业算法

* lst.merge(lst2)
* lst.merge(lst2, comp)
* lst.remove(val)
* lst.remove_if(pred)
* lst.reverse()
* lst.sort()
* lst.sort(comp)
* lst.unique()
* lst.unique(pred)

上述算法在通用算法中也存在但是list使用通用实现性能很差，通常在
list和forward_list要使用类似算算法优先使用list专门版本


##4.关联容器
关联容器中的元素是通过key来存储和检索的,顺序容器是通过位置进行
存储和检索

* map
* set
* multimap
* multiset
* unordered_map
* unordered_set
* unordered_multimap
* unordered_multiset

###4.1初始化
**初始化:**

    //空对象
    map<string, size_t> tmap;
    set<string> tset;

    //列表初始化
    set<string> tset1 = {"the", "hello", "wo", "men"};
    map<string, string> tmap1 = {{"name", "shao"},
                                 {"age", "20"},
                                 {"city", "xian"}}

**对于有序关联容器key值类型必须是可比较的, 默认是增序**

###4.2 pair
pair是定义在utility头中的一个类型，能够容纳两个类型不限制的元素

**pair的操作:**

* `pair<T1, T2> p`
* `pair<T1, T2> p(v1, v2)`
* `pair<T1, T2> p = {v1, v2};`
* `make_pair(v1, v2)`
* `p.first`
* `p.second`
* `p1 op p2`
* `p1 == p2`

***

tuple是定义在tuple头中的一个类型，能够容纳多个类型不限制的元素

**tuple的操作:**

* `tuple<T1, T2, T3...> t`
* `tuple<T1, T2, T3...> t = {v1, v2, v3...}`
* `tuple<T1, T2, T3...> t{v1, v2, v3....}`
* `make_tuple(v1, v2, v3)`
* `get<i>(t)`获取第i个参数的值
* `get<i>(t)=v`设置第i个参数的值
* `tuple_size<tupleType>::value`获取指定类型tuple的元素的个数
* `tuple_element<i, tupleType>::type`获取指定类型tuple指定元素的类型

###4.3 关联容器上的操作

* key_type
* mapped_type
* value_type

***

* c.insert(v)
* c.insert(b, e)
* c.insert({a1, a1...})

*** 

* c.erase(k)
* c.erase(p)
* c.erase(b,e)

***

* c.find(k)
* c.count(k)
* c.lower_bound(k) 返回第一个key值不小于k的元素的迭代器
* c.upper_bound(k) 返回第一个key值大于k的元素的迭代器
* c.equal_range(k) 

**map独有操作:**

* c[k] 返回一个k作为key的元素, 如果key不存在,增加k对应的元素并初始化value值
* c.at(k) 带有检测的访问k对应的元素，如果不存在抛出out_of_range异常

**使用unordered容器，当key值无序或者性能测试揭露的问题hash能够解决

**unordered容器管理操作:**

* c.bucket_count() 正在使用bucket的数量
* c.max_bucket_count() 容器中最大bucket的数量
* c.bucket_size(n)第n个bucket中元素的数量
* c.bucket(k) 检测k在哪个bucket里面
* local_iterator访问bucket中元素的迭代器
* const_local_iterator常量版本的bucket迭代器
* c.begin(), c.end()第n个bucket的迭代器
* c.cbegin(n), c.cend(n)
* c.load_factor()平均每个bucket元素个数
* c.max_load_factor()
* c.rehash(n)再哈希阀值
* c.reserve(n)不进行hash情况下容器容纳的元素个数

针对unordered容器使用自定义类型类:

    size_t hasher(const Sales_data &sd)
    {
        return hash<string>() (sd.isbn());
    }
    bool eqOp(const Sqles_data &lha, const Sqles_data &rhs)
    {
        return lhs.isbn() == rhs.isbn();
    }
    unordered_multiset<Sqles_data, decltype(hasher)*, decltype(eqOp)*>

##5.动态内存
动态内存的生命周期取决于我们在哪里创建和再哪里释放,合适的释放动态资源
是当前程序bug出现多的地方, 动态分配的内存需要谨慎的进行管理.

c++11中引入了两个只能指针使得动态内存管理更加容易, 这些定义的智能指针
定义在memeory头文件中

智能指针是模板类型

    //默认构造的只能指针指向空指针
    shared_ptr<string> p1;
    shared_ptr<list<int>> p2;

使用智能指针的方式和普通指针类似

**shared_ptr和unique_ptr通用操作:**

* shared_ptr<T> sp
* unique_ptr<T> up
* `p`使用这作为一个条件，如果p指向一个对象那么为true
* `*p`解引用p获取p所指向的对象
* `p->mem`
* `p.get()`返回p指向对象的普通指针
* swap(p,q)交换p和q两个智能指针的内部指针
* p.swap(q)
* `shared_ptr<T> p(u)`使用一个unique_ptr进行初始化
* `shared_ptr<T> p(q, d)`使用p管理T*类型的q,并使用可调用的d释放
* p.reset()
* p.reset(q) 重置智能指针
* p.reset(q, d)

**shared_ptr特有的操作:**

* make_shared<T>(args)返回一个智能指针指向动态分配的类型T,并且使用args初始化对象
* `shared_ptr<T> p(q)`p指向一个只能指针q的拷贝,增加引用计数
* `p=q`p和q都是只能指针指向相同对象,先将p的引用计数减一,增加q的引用计数
删除p如果p的引用计数为0
* p.unique()当use_count()为1时表示真
* p.use_count()当前指向对象共享的个数(速度慢,只用于调试)

**程序使用动态内存的三种目的:**

* 不知道需要多少对象
* 不知道需要对象的具体类型
* 想要在多个对象内共享数据(共享相同状态)

**使用new和delete管理内存可能存在的问题:**

* 忘记delete内存，导致内存泄露,难以检测内存泄露知道程序长时间运行导致内存耗尽
* 在一个对象已经被释放后继续使用
* 释放同一块内存两次

**使用智能指针能够避免上述三种情况发生**

使用内建指针访问一个被智能指针管理的对象是危险的

**智能指针的可能勿用:**
智能指针能够提供安全方便的处理动态内存的分配,前提是我们合适的使用

* 不要使用同样的内建指针创建多个智能指针
* 不要删除使用get()函数返回的指针
* 不要使用get()去初始化或者重置另一个智能指针
* 如果你使用一个get()返回的指针, 记住当智能指针的引用个数减少到０的
时候前的指针将被释放
* 使用只能指针管理一个资源而不是一个内存的时候传入一个deleter对管理的资源进行
释放


***

**unique_ptr使用**
同一时刻只有一个unique_ptr指向管理的对象,　这个对象将在unique_ptr销毁的时候同时被
释放

* `unique_pt<T> ul`
* `unique_ptr<T, D> u2`创建空指针，制定删除器类型
* `unique_ptr<T, D> u(d)`创建空指针,创建删除器类型
* `u = nullptr`删除u指向的对象, u变为nullptr
* u.release()返回u管理的对象指针, u变为nullptr
* u.reset() 删除u管理的对象
* u.reset(q)
* u.reset(nullptr)

**unique_ptr不支持拷贝和赋值创建对象, 可以使用下列方式转移控制权**

    unique_ptr<string> p2(p1.release());
    unique_ptr<string> p3(new string("trex"));
    p2.reset(p3.release())

***

**weak_ptr使用**
weak_ptr是一种不控制指向对象生命周期的智能指针, weak_ptr指向一个被shared_ptr
管理的智能指针, 绑定一个weak_ptr到一个shared_ptr不改变引用计数

* `weak_ptr<T> w`
* `weak_ptr<T> w(sp)`
* `w = p`
* w.reset()
* w.use_count()
* w.expired()  如果use_count()为0则为true
* w.lock() 

***

大多数应用应该使用标准库容器而不是动态分布数组

##6. bitset
bitset头中定义了针对任意数量位进行操作和管理的类bitset

* `bitset<n> b`创建一个n位,所有位都置0的bitset
* `bitset<n> b(u)`
* `bitset<n> b(s, pos, m, zero, one)`
* `bitset<cp, pos, m, zero, one>`
* `b.any()`任意位置位
* `b.all()`所有位置位
* `b.none()`没有位置位
* `b.count()`置为的位数
* `b.size()`b中的总位数
* `b.test(pos)`测试pos位置的位是否置位
* `b.set(pos, v)`设置pos位置的位为v
* `b.set()`
* `b.reset(pos)`
* `b.reset()`
* `b.flip(pos)`指定pos位翻转
* `b.flip()`所有位反转
* `b[pos]`
* `b.to_ulong()`
* `b.to_ullong()`
* `b.to_string(zero, one)`将bitset转换为字符串
* `os << b`
* `is >> b`

**n必须是常量**

##7. 正则表达式
正则表达式定义在regex头中

* regex 表示一个正则表达式
* regex_match 匹配符合正则表达式的字符串
* regex_search 找到第一个匹配的字符串
* regex_replace 使用给定的格式替换正则表达式
* sregex_iterator 迭代器适配器调用regex_search迭代所有匹配
* smatch 表示一次搜索的结果
* ssub_match 表示一个子表达式的匹配

##8. 随机数

