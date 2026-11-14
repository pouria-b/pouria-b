from collections import defaultdict
import heapq


def coin_change_greedy(coins, amount):
    result = []
    for coin in sorted(coins, reverse=True):
        while amount >= coin:
            amount -= coin
            result.append(coin)
    return result


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def huffman_coding(text):
    if not text:
        return {}
    freq = defaultdict(int)
    for ch in text:
        freq[ch] += 1

    heap = [HuffmanNode(ch, f) for ch, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    root = heap[0]
    codes = {}

    def generate(node, code=""):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = code or "0"
            return
        generate(node.left, code + "0")
        generate(node.right, code + "1")

    generate(root)
    return codes