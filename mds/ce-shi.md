title: 你好
tags: 测试
date: 2014-11-26
***
我们热爱生活
```
#include <iostream>
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
```

