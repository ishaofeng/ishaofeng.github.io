title: SearchInRotatedSortedArray
tags: LeetCode
date: 2014-11-05
***

>Suppose a sorted array is rotated at some pivot unknown to you beforehand.
>(i.e., 0 1 2 4 5 6 7 might become 4 5 6 7 0 1 2).
>You are given a target value to search. If found in the array return its index, otherwise return -1.
>You may assume no duplicate exists in the array.

对问题进行分析，该问题与对有序序列进行查找的二分查找类似需要考虑的是在分的时候的特殊情况，A为序列数组，start,end分别是区间的开始和技术，`mid=(start+end)>>1`为区间的中间，mid将区间非为有序区间和无须区间两个部分，两个部分成为sec1,sec2,进行处理时存在一下情况: (考虑改变end的方向)

1. `A[mid] == target`此时找到结果
2. `A[start]<A[end]`此时区间为递增区间使用与二法查找一致的比较方式, `target<A[mid]`
3. target落在sec1(`target > A[end]`),此时mid可能在sec1,也可能在sec2
    * mid在sec1(`A[mid] > A[end]`),且此时`target<A[mid]`时end减小
    * mid在sec2(`A[mid] < A[end]`)
4. target落在sec2(`target < A[end]`),此时需要mid在sec2并且`target<A[mid]`时end减小

最终代码如下:

    int search(int A[], int n, int target)
    {
        if (NULL == A)
        {
            return -1;
        }

        int start = 0;
        int end = n - 1;
        int mid;

        while (start <= end)
        {
            mid = (start + end) >> 1;
            if (A[mid] == target)
            {
                return mid;
            }
            else if (A[start] < A[end] && target < A[mid] || target > A[end] \
                && (A[mid] < A[end] || target < A[mid]) || A[mid] < A[end] && target < A[mid])
            {
                end = mid - 1;
            }
            else
            {
                start = mid + 1;
            }
        }

        return -1;
    }

