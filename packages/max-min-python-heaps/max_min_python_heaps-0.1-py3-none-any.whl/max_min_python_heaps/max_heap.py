import heapq
class MaxHeap:
    @staticmethod
    def add(heap, num):
        heapq.heappush(heap, -1*num)
    @staticmethod
    def peak(heap):
        return heap[0] * -1
    @staticmethod
    def pop(heap):
        return heapq.heappop(heap) * -1
    @staticmethod
    def heapify(heap):
        heapq.heapify(heap)
    @staticmethod
    def merge(heap_1, heap_2):
        heapq.merge(heap_1, heap_2)
