import heapq
import numpy as np
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
        myneglist = [ -x for x in heap]
        heapq.heapify(myneglist)
        myposlist = [ -1 * x for x in heap]
        return myposlist
    @staticmethod
    def merge(heap_1, heap_2):
        heapq.merge(heap_1, heap_2)
