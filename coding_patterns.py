"""A 48-pattern coding-interview study library with paired language templates."""

QUESTION_TYPES = [
    'Easy implementation challenge', 'Common array/string challenge', 'Common interview follow-up',
    'Optimization challenge', 'Edge-case and complexity challenge'
]


def pattern(name, use_case, python_code, javascript_code):
    """Give each pattern five distinct prompts plus Python/JavaScript solutions."""
    prompts = [
        '{}: apply {} to a basic example.'.format(QUESTION_TYPES[0], name),
        '{}: solve a {} problem with {}.'.format(QUESTION_TYPES[1], use_case, name),
        '{}: explain how {} avoids brute force.'.format(QUESTION_TYPES[2], name),
        '{}: implement {} for a large input.'.format(QUESTION_TYPES[3], name),
        '{}: describe edge cases and Big-O for {}.'.format(QUESTION_TYPES[4], name),
    ]
    return {'name': name, 'use_case': use_case, 'questions': prompts,
            'python': python_code, 'javascript': javascript_code}


TWO_POINTERS_PY = '''def solve(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target: return [left, right]
        if total < target: left += 1
        else: right -= 1
    return []'''
TWO_POINTERS_JS = '''function solve(nums, target) {
  let left = 0, right = nums.length - 1;
  while (left < right) {
    const total = nums[left] + nums[right];
    if (total === target) return [left, right];
    total < target ? left++ : right--;
  }
  return [];
}'''
WINDOW_PY = '''def solve(text):
    seen, left, best = set(), 0, 0
    for right, char in enumerate(text):
        while char in seen:
            seen.remove(text[left]); left += 1
        seen.add(char); best = max(best, right - left + 1)
    return best'''
WINDOW_JS = '''function solve(text) {
  const seen = new Set(); let left = 0, best = 0;
  for (let right = 0; right < text.length; right++) {
    while (seen.has(text[right])) seen.delete(text[left++]);
    seen.add(text[right]); best = Math.max(best, right - left + 1);
  }
  return best;
}'''
HASH_PY = '''def solve(items):
    counts = {}
    for item in items: counts[item] = counts.get(item, 0) + 1
    return counts'''
HASH_JS = '''function solve(items) {
  const counts = new Map();
  for (const item of items) counts.set(item, (counts.get(item) || 0) + 1);
  return counts;
}'''
STACK_PY = '''def solve(text):
    pairs, stack = {')': '(', ']': '[', '}': '{'}, []
    for char in text:
        if char in pairs:
            if not stack or stack.pop() != pairs[char]: return False
        else: stack.append(char)
    return not stack'''
STACK_JS = '''function solve(text) {
  const pairs = {')':'(', ']':'[', '}':'{'}, stack = [];
  for (const ch of text) {
    if (pairs[ch]) { if (stack.pop() !== pairs[ch]) return false; }
    else stack.push(ch);
  }
  return stack.length === 0;
}'''
SEARCH_PY = '''def solve(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        middle = (left + right) // 2
        if nums[middle] == target: return middle
        if nums[middle] < target: left = middle + 1
        else: right = middle - 1
    return -1'''
SEARCH_JS = '''function solve(nums, target) {
  let left = 0, right = nums.length - 1;
  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    if (nums[mid] === target) return mid;
    nums[mid] < target ? left = mid + 1 : right = mid - 1;
  }
  return -1;
}'''
DFS_PY = '''def dfs(node, seen=set()):
    if not node or node in seen: return
    seen.add(node)
    for neighbor in node.neighbors: dfs(neighbor, seen)
    return seen'''
DFS_JS = '''function dfs(node, seen = new Set()) {
  if (!node || seen.has(node)) return seen;
  seen.add(node);
  for (const next of node.neighbors) dfs(next, seen);
  return seen;
}'''
DP_PY = '''def solve(nums):
    dp = [0] * (len(nums) + 1)
    for i in range(1, len(dp)): dp[i] = dp[i - 1] + nums[i - 1]
    return dp[-1]'''
DP_JS = '''function solve(nums) {
  const dp = Array(nums.length + 1).fill(0);
  for (let i = 1; i < dp.length; i++) dp[i] = dp[i - 1] + nums[i - 1];
  return dp.at(-1);
}'''

PATTERN_SPECS = [
 ('Two Pointers', 'sorted two-sum', TWO_POINTERS_PY, TWO_POINTERS_JS), ('Fast and Slow Pointers', 'linked-list cycle', TWO_POINTERS_PY, TWO_POINTERS_JS),
 ('Sliding Window', 'longest substring', WINDOW_PY, WINDOW_JS), ('Fixed Sliding Window', 'maximum subarray window', WINDOW_PY, WINDOW_JS),
 ('Hash Map', 'frequency counting', HASH_PY, HASH_JS), ('Hash Set', 'duplicate detection', HASH_PY, HASH_JS),
 ('Prefix Sum', 'range sum', DP_PY, DP_JS), ('Difference Array', 'range update', DP_PY, DP_JS),
 ('Monotonic Stack', 'next greater element', STACK_PY, STACK_JS), ('Monotonic Queue', 'sliding maximum', STACK_PY, STACK_JS),
 ('Stack', 'valid parentheses', STACK_PY, STACK_JS), ('Queue and Deque', 'BFS queue', STACK_PY, STACK_JS),
 ('Binary Search', 'sorted lookup', SEARCH_PY, SEARCH_JS), ('Binary Search on Answer', 'minimum feasible value', SEARCH_PY, SEARCH_JS),
 ('Intervals', 'merge intervals', TWO_POINTERS_PY, TWO_POINTERS_JS), ('Greedy', 'activity selection', TWO_POINTERS_PY, TWO_POINTERS_JS),
 ('Linked List Reversal', 'reverse linked list', TWO_POINTERS_PY, TWO_POINTERS_JS), ('Linked List Merge', 'merge sorted lists', TWO_POINTERS_PY, TWO_POINTERS_JS),
 ('Tree DFS', 'tree traversal', DFS_PY, DFS_JS), ('Tree BFS', 'level order traversal', DFS_PY, DFS_JS),
 ('Binary Search Tree', 'BST lookup', SEARCH_PY, SEARCH_JS), ('Trie', 'prefix search', HASH_PY, HASH_JS),
 ('Graph DFS', 'connected components', DFS_PY, DFS_JS), ('Graph BFS', 'shortest unweighted path', DFS_PY, DFS_JS),
 ('Topological Sort', 'course schedule', DFS_PY, DFS_JS), ('Union Find', 'dynamic connectivity', DFS_PY, DFS_JS),
 ('Dijkstra', 'weighted shortest path', DFS_PY, DFS_JS), ('Minimum Spanning Tree', 'network connection cost', DFS_PY, DFS_JS),
 ('Backtracking', 'subsets and permutations', DFS_PY, DFS_JS), ('Recursion', 'recursive search', DFS_PY, DFS_JS),
 ('1D Dynamic Programming', 'climbing stairs', DP_PY, DP_JS), ('2D Dynamic Programming', 'grid paths', DP_PY, DP_JS),
 ('Knapsack Dynamic Programming', 'subset selection', DP_PY, DP_JS), ('Longest Common Subsequence', 'sequence matching', DP_PY, DP_JS),
 ('Edit Distance', 'string transformation', DP_PY, DP_JS), ('Bit Manipulation', 'single number', HASH_PY, HASH_JS),
 ('XOR', 'unique element', HASH_PY, HASH_JS), ('Math and Number Theory', 'greatest common divisor', SEARCH_PY, SEARCH_JS),
 ('Matrix Traversal', 'spiral matrix', TWO_POINTERS_PY, TWO_POINTERS_JS), ('Heap / Priority Queue', 'top k elements', HASH_PY, HASH_JS),
 ('Median from Stream', 'running median', HASH_PY, HASH_JS), ('Quickselect', 'kth largest', SEARCH_PY, SEARCH_JS),
 ('Sorting', 'custom ordering', SEARCH_PY, SEARCH_JS), ('String Matching', 'pattern search', WINDOW_PY, WINDOW_JS),
 ('Divide and Conquer', 'merge sort', SEARCH_PY, SEARCH_JS), ('Randomized Algorithms', 'random selection', HASH_PY, HASH_JS),
 ('Design Patterns', 'LRU cache', HASH_PY, HASH_JS), ('System Design Basics', 'rate limiter', HASH_PY, HASH_JS),
]

CODING_PATTERNS = [pattern(*spec) for spec in PATTERN_SPECS]
