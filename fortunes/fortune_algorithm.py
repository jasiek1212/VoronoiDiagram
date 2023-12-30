from .tree import *
from enum import Enum
from queue import PriorityQueue
import math

class BeachlineItemType(Enum):
    NONE = 0
    ARC = 1
    EDGE = 2

class Vector2:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class Edge:
    def __init__(self) -> None:
        self.start = Vector2()
        self.direction = Vector2()
        self.extendsUpwardsForever = False


class CompleteEdge:
    def __init__(self) -> None:
        self.endpointA = Vector2()
        self.endpointB = Vector2()


class Arc:
    def __init__(self) -> None:
        self.focus = Vector2()
        self.squeezeEvent = None


class BeachLineItem:
    def __init__(self) -> None:
        self.type = BeachlineItemType.NONE
        self.arc = Arc()
        self.edge = Edge()

        self.parent = None
        self.left = None
        self.right = None
    

    def set_left(self, new_left):
        assert self.type == BeachlineItemType.EDGE
        assert new_left is not None

        self.left = new_left
        new_left.parent = self
    

    def set_right(self, new_right):
        assert self.type == BeachlineItemType.EDGE
        assert new_right is not None

        self.right = new_right
        new_right.parent = self
    

    def set_parent_from_item(self, item):
        assert item is not None
        if item.parent is None:
            self.parent = None
        else:
            if item.parent.left == item:
                item.parent.set_left(self)
            else:
                assert item.parent.right == item
                item.parent.set_right(self)


class SweepEventType(Enum):
    NONE = 0
    NEW_POINT = 1
    EDGE_INTERSECTION = 2


class NewPointEvent:
    def __init__(self) -> None:
        self.point = Vector2()


class EdgeIntersectionEvent:
    def __init__(self) -> None:
        self.intersection_point = Vector2()
        self.squeezed_arc = None
        self.is_valid = False


class SweepEvent:
    def __init__(self) -> None:
        self.y_coord = 0
        self.type = SweepEventType.NONE
        self.new_point = NewPointEvent()
        self.edge_intersect = EdgeIntersectionEvent()


class FortuneState:
    def __init__(self) -> None:
        self.sweep_y = 0.0
        self.edges = []
        self.unencountered_events = PriorityQueue()
        self.beachline_root = None

    
    def event_coparision(self, lhs, rhs):
        assert lhs is not None and rhs is not None
        return lhs.y_coord < rhs.y_coord


def calculate_arc_y(arc, x, directrixY):
    a = 1.0 / (2.0 * (arc.focus.y - directrixY))
    c = (arc.focus.y + directrixY) * 0.5
    w = x - arc.focus.x

    return a * w * w + c


def get_edge_arc_intersection(edge: Edge, arc: Arc, directrixY, intersection_point):
    
    # special case: edge is a vertical line
    if edge.direction.x == 0.0:
        if directrixY == arc.focus.y:
            if edge.start.x == arc.focus.x:
                intersection_point.x = arc.focus.x
                intersection_point.y = arc.focus.y
                return True
            else:
                return False

        arc_y = calculate_arc_y(arc, edge.start.x, directrixY)
        intersection_point.x = edge.start.x
        intersection_point.y = arc_y

        return True

    # y = px + q
    p = edge.direction.y / edge.direction.x
    q = edge.start.y - p * edge.start.x

    # special case: arc is a vertical line (directrix_y == arc.focus.y)
    if arc.focus.y == directrixY:
        intersection_x_offset = arc.focus.x - edge.start.x
        # check if intersection is in the direction that the edge is going
        if intersection_x_offset * edge.direction.x < 0:
            return False
        
        intersection_point.x = arc.focus.x
        intersection_point.y = p * arc.focus.x + q
        return True
    

    # general case: solving quadratic equation y = a_0 + a_1x + a_2x^2

    a2 = 1.0 / (2.0 * (arc.focus.y - directrixY))
    a1 = -p - 2.0 * a2 * arc.focus.x
    a0 = a2 * arc.focus.x ** 2 + (arc.focus.y + directrixY) * 0.5 - q

    discriminant = a1 ** 2 - 4 * a2 * a0

    if discriminant < 0:
        return False 

    root_disc = math.sqrt(discriminant)
    x1 = (-a1 + root_disc) / (2.0 * a2)
    x2 = (-a1 - root_disc) / (2.0 * a2)

    x1_offset = x1 - edge.start.x
    x2_offset = x2 - edge.start.x
    x1_dot = x1_offset * edge.direction.x
    x2_dot = x2_offset * edge.direction.x

    # find correct x value based on the direction
    if x1_dot >= 0.0 and x2_dot < 0.0:
        x = x1
    elif x1_dot < 0.0 and x2_dot >= 0.0:
        x = x2
    elif x1_dot >= 0.0 and x2_dot >= 0.0:
        x = x1 if x1_dot < x2_dot else x2
    else:  # x1Dot < 0.0 and x2Dot < 0.0
        x = x2 if x1_dot < x2_dot else x1
    
    y = calculate_arc_y(arc, x, directrixY)
    assert math.isfinite(y)
    intersection_point.x = x
    intersection_point.y = y
    return True


def get_active_arc_for_x(root, x, directrix_y):
    current_item = root
    while current_item.type != BeachlineItemType.ARC:
        assert current_item.type == BeachlineItemType.EDGE
        left = get_first_left_leaf(current_item)
        right = get_first_left_leaf(current_item)
        assert left is not None and left.type == BeachlineItemType.ARC
        assert right is not None and right.type == BeachlineItemType.ARC

        from_left = get_first_right_parent(left)
        from_right = get_first_left_parent(right)
        assert from_left is not None and from_left == from_right
        assert from_left.type == BeachlineItemType.EDGE
        separating_edge = from_left.edge

        left_intersect = Vector2()
        right_intersect = Vector2()
        did_left_intersect = get_edge_arc_intersection(separating_edge, left.arc, directrix_y, left_intersect)
        did_right_intersect = get_edge_arc_intersection(separating_edge, right.arc, directrix_y, right_intersect)

        intersection_x = left_intersect.x
        if not did_left_intersect and did_right_intersect:
            intersection_x = right_intersect.x
        
        if x < intersection_x:
            current_item = current_item.left
        else:
            current_item = current_item.right
    
    assert current_item.type == BeachlineItemType.ARC
    return current_item


def create_arc(focus: Vector2):
    result = BeachLineItem()
    result.type = BeachlineItemType.ARC
    result.arc.focus = focus
    result.arc.squeezeEvent = None

    return result


def create_edge(start, direction):
    result = BeachLineItem()
    result.type = BeachlineItemType.EDGE
    result.edge.start = start
    result.edge.direction = direction
    result.edge.extendsUpwardsForever = False
    return result


def try_get_edge_intersection(e1: Edge, e2: Edge, intersection_point: Vector2):
    dx = e2.start.x - e1.start.x
    dy = e2.start.y - e1.start.y
    det = e2.direction.x * e1.direction.y - e2.direction.y * e1.direction.x
    if det == 0:
        return False  # Parallel or coincident lines

    u = (dy * e2.direction.x - dx * e2.direction.y) / det
    v = (dy * e1.direction.x - dx * e1.direction.y) / det

    if u < 0.0 and not e1.extendsUpwardsForever:
        return False
    if v < 0.0 and not e2.extendsUpwardsForever:
        return False
    if u == 0.0 and v == 0.0 and not e1.extendsUpwardsForever and not e2.extendsUpwardsForever:
        return False

    intersection_point.x = e1.start.x + e1.direction.x * u
    intersection_point.y = e1.start.y + e1.direction.y * u
    return True


def add_arc_squeeze_event(event_queue: PriorityQueue, arc: Arc):
    left_edge = get_first_left_parent(arc)
    right_edge = get_first_right_parent(arc)

    if left_edge is None or right_edge is None:
        return
    
    circle_event_point = Vector2()
    edges_intersect = try_get_edge_intersection(left_edge.edge, right_edge.edge, circle_event_point)
    if not edges_intersect:
        return
    
    circle_centre_offset = Vector2(arc.focus.x - circle_event_point.x, arc.focus.y - circle_event_point.y)
    circle_radius = math.hypot(circle_centre_offset.x, circle_centre_offset.y)
    circle_event_y = circle_event_point.y - circle_radius
    assert arc.type == BeachlineItemType.ARC

    if arc.squeezeEvent is not None:
        if arc.squeezeEvent.y_coord >= circle_event_y:
            return
        else:
            assert arc.squeezeEvent.type == SweepEventType.EDGE_INTERSECTION
            arc.squeezeEvent.edge_intersect.is_valid = False
    
    new_event = SweepEvent()
    new_event.type = SweepEventType.EDGE_INTERSECTION
    new_event.y_coord = circle_event_y
    new_event.edge_intersect.squeezed_arc = arc
    new_event.edge_intersect.intersection_point = circle_event_point
    new_event.edge_intersect.is_valid = True
    event_queue.put(new_event)

    arc.squeezeEvent = new_event


def add_arc_to_beachline(event_queue: PriorityQueue, root, event: SweepEvent, sweep_line_y):
    new_point = event.new_point.point
    replaced_arc = get_active_arc_for_x(root, new_point.x, sweep_line_y)
    assert replaced_arc is not None and replaced_arc.type == BeachlineItemType.ARC


    split_arc_left = create_arc(replaced_arc.focus)
    split_arc_right = create_arc(replaced_arc.focus)
    new_arc = create_arc(new_point)

    intersection_y = calculate_arc_y(replaced_arc, new_point.x, sweep_line_y)
    assert math.isfinite(intersection_y)
    edge_start = Vector2(new_point.x, intersection_y)
    focus_offset = Vector2(new_arc.focus.x - replaced_arc.focus.x, new_arc.focus.y - replaced_arc.focus.y)

    edge_dir = normalize(Vector2(focus_offset.y, -focus_offset.x))
    edge_left = create_edge(edge_start, edge_dir)
    edge_right = create_edge(edge_start, Vector2(-edge_dir.x, -edge_dir.y))

    assert replaced_arc.left is None and replaced_arc.right is None
    edge_left.set_parent_from_item(replaced_arc)
    edge_left.set_left(split_arc_left)
    edge_left.set_right(edge_right)
    edge_right.set_left(new_arc)
    edge_right.set_right(split_arc_right)

    new_root = root
    if root == replaced_arc:
        new_root = edge_left

    if replaced_arc.arc.squeezeEvent is not None:
        assert replaced_arc.arc.squeezeEvent.type == SweepEventType.EDGE_INTERSECTION
        replaced_arc.arc.squeezeEvent.edgeIntersect.isValid = False
        # In Python, there's no need to explicitly delete objects

    # Assume VerifyThatThereAreNoReferencesToItem is implemented elsewhere
    check_no_references_to_item(new_root, replaced_arc)

    add_arc_squeeze_event(event_queue, split_arc_left)
    add_arc_squeeze_event(event_queue, split_arc_right)

    return new_root


def normalize(vector):
    length = math.sqrt(vector.x**2 + vector.y**2)
    return Vector2(vector.x / length, vector.y / length) if length != 0 else Vector2(0, 0)


def remove_arc_from_beachline(event_queue: PriorityQueue, root: BeachLineItem, output_edges: list[CompleteEdge], event: SweepEvent):
    squeezed_arc = event.edge_intersect.squeezed_arc
    assert event.type == SweepEventType.EDGE_INTERSECTION
    assert event.edge_intersect.is_valid
    assert squeezed_arc.squeezeEvent == event

    left_edge = get_first_left_parent(squeezed_arc)
    right_edge = get_first_right_parent(squeezed_arc)
    assert left_edge is not None and right_edge is not None

    left_arc = get_first_left_leaf(left_edge)
    right_arc = get_first_right_leaf(right_edge)
    assert left_arc is not None and right_arc is not None
    assert left_arc != right_arc

    circle_centre = event.edge_intersect.intersection_point
    edge_a = CompleteEdge()
    edge_a.endpointA = left_edge.edge.start
    edge_a.endpointB = circle_centre
    edge_b = CompleteEdge()
    edge_b.endpointA = circle_centre
    edge_b.endpointB = right_edge.edge.start

    if left_edge.edge.extendsUpwardsForever:
        edge_a.endpointA.y = float('inf')
    if right_edge.edge.extendsUpwardsForever:
        edge_b.endpointA.y = float('inf')

    output_edges.append(edge_a)
    output_edges.append(edge_b)

    adjacent_arc_offset = Vector2(right_arc.arc.focus.x - left_arc.arc.focus.x,
                                  right_arc.arc.focus.y - left_arc.arc.focus.y)
    new_edge_direction = Vector2(adjacent_arc_offset.y, -adjacent_arc_offset.x)
    new_edge_direction = normalize(new_edge_direction)

    new_item = create_edge(circle_centre, new_edge_direction)

    higher_edge = None
    temp_item = squeezed_arc
    while temp_item.parent is not None:
        temp_item = temp_item.parent
        if temp_item == left_edge:
            higher_edge = left_edge
        if temp_item == right_edge:
            higher_edge = right_edge

    assert higher_edge is not None and higher_edge.type == BeachlineItemType.EDGE

    new_item.set_parent_from_item(higher_edge)
    new_item.set_left(higher_edge.left)
    new_item.set_right(higher_edge.right)

    remaining_item = None
    parent = squeezed_arc.parent
    if parent.left == squeezed_arc:
        remaining_item = parent.right
    else:
        assert parent.right == squeezed_arc
        remaining_item = parent.left

    assert parent in [left_edge, right_edge]
    assert parent != higher_edge

    remaining_item.set_parent_from_item(parent)

    new_root = root
    if root in [left_edge, right_edge]:
        new_root = new_item

    check_no_references_to_item(new_root, left_edge)
    check_no_references_to_item(new_root, squeezed_arc)
    check_no_references_to_item(new_root, right_edge)

    if squeezed_arc.arc.squeezeEvent is not None:
        squeezed_arc.arc.squeezeEvent.edgeIntersect.isValid = False

    add_arc_squeeze_event(event_queue, left_arc)
    add_arc_squeeze_event(event_queue, right_arc)

    return new_root


def finish_edge(item: BeachLineItem, edges: list[CompleteEdge], length=1000):
    if item is None:
        return
    
    if item.type == BeachlineItemType.EDGE:
        edge_end = Vector2(item.edge.start.x + length * item.edge.direction.x,
                           item.edge.start.y + length * item.edge.direction.y)
        
        edge = CompleteEdge()
        edge.endpointA = item.edge.start
        edge.endpointB = edge_end
        edges.append(edge)

        finish_edge(item.left, edges, length)
        finish_edge(item.right, edges, length)


def fortunes_algorithm(sites: list[Vector2], cutoffY: float):
    edges = []
    event_queue = PriorityQueue()
    for point in sites:
        event = SweepEvent()
        event.type = SweepEventType.NEW_POINT
        event.new_point.point = point
        event.y_coord = point.y
        event_queue.put((event.y_coord, event))
    

    first_event_y, first_event = event_queue.get()
    assert first_event.type == SweepEventType.NEW_POINT

    if first_event_y < cutoffY:
        result = FortuneState()
        result.sweep_y = cutoffY
        while not event_queue.empty():
            _, event = event_queue.get()
            result.unencountered_events.append(event)
        
        return result

    first_arc = create_arc(first_event.new_point.point)
    root = first_arc
    startup_special_case_end_y = first_arc.arc.focus.y - 1.0

    while not event_queue.empty():
        event_y, event = event_queue.get()
        if event_y < cutoffY or event_y <= startup_special_case_end_y:
            break
            
        if event.type == SweepEventType.NEW_POINT:
            root = add_arc_to_beachline(event_queue, root, event, event_y)
        elif event.type == SweepEventType.EDGE_INTERSECTION and event.edge_intersect.is_valid:
            if event.edge_intersect.is_valid:
                root = remove_arc_from_beachline(event_queue, root, edges, event)
        else:
            print("Unrecognised queue item type: ", event.type)
    
    if event_queue.empty() or cutoffY < -200.0:
        finish_edge(root, edges)
    
    result = FortuneState()
    result.sweep_y = 0.0
    result.beachline_root = root
    result.edges = edges

    while not event_queue.empty():
        _, event = event_queue.get()
        result.unencountered_events.append(event)
    
    return result


