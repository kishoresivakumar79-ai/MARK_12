"""
Priority Manager and Tree Structure for MARK 12 Task System
Implements:
- Priority Queue: Tasks ordered by urgency and deadline using heapq
- Tree: Hierarchical task structure (Parent-Child relationships)
"""
import heapq
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

@dataclass(order=True)
class PrioritizedTask:
    priority: int  # 1 = Urgent/Critical, 5 = Low
    timestamp: float = field(compare=True)
    task_id: str = field(compare=False)
    data: Dict[str, Any] = field(compare=False)

class TaskPriorityQueue:
    """Priority Queue implementing O(log N) scheduling."""
    def __init__(self):
        self._heap: List[PrioritizedTask] = []
        self._task_map: Dict[str, PrioritizedTask] = {}

    def push(self, task_id: str, priority: int, data: Dict[str, Any]):
        item = PrioritizedTask(priority=priority, timestamp=time.time(), task_id=task_id, data=data)
        heapq.heappush(self._heap, item)
        self._task_map[task_id] = item

    def pop(self) -> Optional[Dict[str, Any]]:
        while self._heap:
            item = heapq.heappop(self._heap)
            if item.task_id in self._task_map:
                del self._task_map[item.task_id]
                return item.data
        return None

    def peek(self) -> Optional[Dict[str, Any]]:
        return self._heap[0].data if self._heap else None

    def get_all_sorted(self) -> List[Dict[str, Any]]:
        """Return tasks sorted by priority without mutating the heap."""
        sorted_items = sorted(self._heap)
        return [item.data for item in sorted_items]

    def remove(self, task_id: str) -> bool:
        if task_id in self._task_map:
            del self._task_map[task_id]
            # Will be lazily discarded on pop
            return True
        return False

    def __len__(self):
        return len(self._task_map)


class TaskTreeNode:
    """Tree node representing hierarchical tasks and subtasks."""
    def __init__(self, task_data: Dict[str, Any]):
        self.task_id = task_data.get("id")
        self.data = task_data
        self.parent_id = task_data.get("parent_id")
        self.children: List['TaskTreeNode'] = []

    def add_child(self, child_node: 'TaskTreeNode'):
        self.children.append(child_node)

    def to_dict(self) -> Dict[str, Any]:
        node_dict = dict(self.data)
        node_dict["children"] = [c.to_dict() for c in self.children]
        return node_dict

class TaskTree:
    """Hierarchical Task Tree."""
    def __init__(self, raw_tasks: List[Dict[str, Any]]):
        self.nodes: Dict[str, TaskTreeNode] = {t["id"]: TaskTreeNode(t) for t in raw_tasks}
        self.roots: List[TaskTreeNode] = []

        for node in self.nodes.values():
            if node.parent_id and node.parent_id in self.nodes:
                self.nodes[node.parent_id].add_child(node)
            else:
                self.roots.append(node)

    def get_hierarchy(self) -> List[Dict[str, Any]]:
        return [root.to_dict() for root in self.roots]

    def get_subtasks(self, task_id: str) -> List[Dict[str, Any]]:
        if task_id not in self.nodes:
            return []
        
        result = []
        def traverse(node: TaskTreeNode):
            for child in node.children:
                result.append(child.data)
                traverse(child)
        
        traverse(self.nodes[task_id])
        return result
