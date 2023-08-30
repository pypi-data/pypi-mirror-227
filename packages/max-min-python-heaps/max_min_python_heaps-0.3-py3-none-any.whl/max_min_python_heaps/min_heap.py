import heapq
class MinHeap:
    @staticmethod
    def add(heap, num):
        heapq.heappush(heap, num)
    @staticmethod
    def peak(heap):
        return heap[0]
    @staticmethod
    def pop(heap):
        heapq.heappop(heap)
    @staticmethod
    def heapify(heap):
        return heapq.heapify(heap)
    @staticmethod
    def merge(heap_1, heap_2):
        heapq.merge(heap_1, heap_2)

