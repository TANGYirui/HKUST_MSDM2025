
class QuickSort:
    """
    Quick sort Implementation
    Use 3-way partitioning
    """
    
    def sort(self, arr):
        if not arr:  # 防御性检查
            return
        self._quicksort(arr, 0, len(arr) - 1)
    
    def _quicksort(self, arr, low, high):
        """
        We use 3-way partitioning (Dijkstra's algorithm)
        """
        if low >= high:
            return
        
        lt = low     
        i = low + 1  
        gt = high      
        pivot = arr[low]  
        
        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif arr[i] > pivot:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1
            else:
                i += 1
        
        # recursion 
        self._quicksort(arr, low, lt - 1)
        self._quicksort(arr, gt + 1, high)

    # keep traditional partition scheme (optional)
    def _partition_lomuto(self, arr, low, high):
        """Less efficient Lomuto partition scheme (for educational purposes)"""
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
class MergeSort:
    """归并排序类 - 非原地实现（返回新数组）"""
    
    def sort(self, arr):
        """
        公共排序接口
        :param arr: 输入列表
        :return: 新的已排序列表（不修改原数组）
        """
        if not arr:  # 防御性检查
            return []
        return self._merge_sort(arr)
    
    def _merge_sort(self, arr):
        """递归分治排序"""
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = self._merge_sort(arr[:mid])   # 递归排序左半
        right = self._merge_sort(arr[mid:])  # 递归排序右半
        return self._merge(left, right)      # 合并结果
    
    def _merge(self, left, right):
        """合并两个已排序数组"""
        result = []
        i = j = 0
        
        # 比较合并
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        # 追加剩余部分
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
class HeapSort:
    """工业级堆排序实现 - 原地排序（O(1)额外空间）"""
    
    def sort(self, arr):
        """
        原地堆排序（修改输入数组）
        :param arr: 要排序的列表
        :return: None（直接修改原始数组）
        """
        if not arr:  # 防御性空检查
            return
        
        n = len(arr)
        
        # 1. 构建最大堆（从最后一个非叶子节点开始）
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i)
        
        # 2. 逐个提取最大元素到末尾
        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]  # 交换堆顶和末尾
            self._heapify(arr, i, 0)         # 重新调整堆（排除已排序部分）
    
    def _heapify(self, arr, n, i):
        """
        调整以i为根的子树为最大堆（迭代实现 - 避免递归栈溢出）
        :param arr: 数组
        :param n: 堆的有效大小
        :param i: 当前根节点索引
        """
        while True:
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            # 比较左右子节点
            if left < n and arr[left] > arr[largest]:
                largest = left
            if right < n and arr[right] > arr[largest]:
                largest = right
            
            # 无需调整则终止
            if largest == i:
                break
            
            # 交换并继续向下调整
            arr[i], arr[largest] = arr[largest], arr[i]
            i = largest  # 更新当前节点为交换后的位置
    
    # 非原地排序接口（可选）
    def sorted(self, arr):
        """
        函数式接口：返回新排序数组（不修改原数组）
        :return: 新的已排序列表
        """
        if not arr:
            return []
        new_arr = arr.copy()  # 创建副本避免副作用
        self.sort(new_arr)    # 原地排序副本
        return new_arr
    
class CountingSort:
    """计数排序类 - 支持负数/稳定性保证/范围优化"""
    
    def sort(self, arr):
        """
        原地计数排序（修改输入数组）
        :param arr: 整数列表
        :raises ValueError: 非整数元素
        :raises MemoryError: 值域过大
        """
        if not arr:
            return
        
        if not all(isinstance(x, int) for x in arr):
            raise ValueError("计数排序仅支持整数数组")
        
        min_val, max_val = min(arr), max(arr)
        self._validate_range(min_val, max_val)
        
        self._stable_counting_sort(arr, min_val, max_val)
    
    def sorted(self, arr):
        """
        函数式接口：返回新排序数组（不修改原数组）
        :return: 新的已排序列表
        """
        if not arr:
            return []
        new_arr = arr.copy()
        self.sort(new_arr)
        return new_arr
    
    def _validate_range(self, min_val, max_val, max_range=10_000_000):
        """
        防御性检查：防止值域过大导致内存爆炸
        :param max_range: 最大允许范围（默认1000万）
        """
        range_size = max_val - min_val + 1
        if range_size > max_range:
            raise MemoryError(
                f"值域过大 ({range_size:,} 个唯一值)，"
                f"超过安全阈值 {max_range:,}。"
                "考虑改用快速排序或归并排序。"
            )
    
    def _stable_counting_sort(self, arr, min_val, max_val):
        """稳定计数排序核心实现"""
        n = len(arr)
        range_size = max_val - min_val + 1
        

        count = [0] * range_size
        
        for num in arr:
            count[num - min_val] += 1
        
        for i in range(1, range_size):
            count[i] += count[i - 1]
        
        output = [0] * n
        for i in range(n - 1, -1, -1):
            num = arr[i]
            pos = count[num - min_val] - 1
            output[pos] = num
            count[num - min_val] -= 1
        
        for i in range(n):
            arr[i] = output[i]