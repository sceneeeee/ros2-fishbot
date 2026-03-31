from geometry_msgs.msg import PoseStamped,Pose
from nav2_simple_commander.robot_navigator import BasicNavigator,TaskResult
import rclpy
from rclpy.node import Node
import rclpy.time
from tf2_ros import TransformListener, Buffer # TF变换监听器
from geometry_msgs.msg import TransformStamped # 消息接口
from tf_transformations import euler_from_quaternion,quaternion_from_euler # 四元数转欧拉角, 欧拉角转四元数
from rclpy.duration import Duration
import math # 角度转弧度
from autopatrol_interfaces.srv import SpeechText

class PatrolNode(BasicNavigator):
    def __init__(self, node_name="patrol_node"):
        super().__init__(node_name)
        self.declare_parameter('initial_point', [0.0, 0.0, 0.0])
        self.declare_parameter('patrol_points', [
            0.0, 0.0, 0.0, 
            1.0, 1.0, 1.57
            ])
        self.initial_point = self.get_parameter('initial_point').value
        self.patrol_points = self.get_parameter('patrol_points').value
        self.buffer_ = Buffer() # 创建TF变换缓冲区
        self.listener_ = TransformListener(self.buffer_, self) # 创建TF变换监听器
        self.speech_client_ = self.create_client(SpeechText, 'speech_text') # 创建语音服务客户端

    def get_pose_by_xyyaw(self, x, y, yaw):
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.pose.position.x = x
        pose.pose.position.y = y
        quat = quaternion_from_euler(0, 0, yaw)
        pose.pose.orientation.x = quat[0]
        pose.pose.orientation.y = quat[1]
        pose.pose.orientation.z = quat[2]
        pose.pose.orientation.w = quat[3]
        return pose
        
    def init_robot_pose(self):
        self.initial_point_ = self.get_parameter('initial_point').value
        init_pose = self.get_pose_by_xyyaw(self.initial_point_[0], 
                                           self.initial_point_[1], 
                                           self.initial_point_[2])
        self.setInitialPose(init_pose)
        self.waitUntilNav2Active()
        
    def get_target_point(self):
        points = []
        self.target_points_ = self.get_parameter('patrol_points').value
        for index in range(int(len(self.target_points_)/3)):
            x = self.target_points_[index*3]
            y = self.target_points_[index*3+1]
            yaw = self.target_points_[index*3+2]
            points.append((x, y, yaw))
            self.get_logger().info(f"Patrol point {index}: x={x}, y={y}, yaw={yaw}")

        return points

    def nav_to_pose(self, target_pose):
        self.goToPose(target_pose)
        while not self.isTaskComplete():
            feedback = self.getFeedback()
            self.get_logger().info(f'Navigating to goal: {feedback.distance_remaining:.2f} meters remaining')
        result = self.getResult()
        self.get_logger().info(f'Navigation result: {result}')



    def get_current_pose(self):
        while rclpy.ok():
            try:
                result = self.buffer_.lookup_transform("map",
                                                        "base_footprint", 
                                                    rclpy.time.Time(seconds=0),
                                                    Duration(seconds=1.0)
                                                    ) # 获取坐标变换
                
                transform = result.transform
                self.get_logger().info(f"translation {transform.translation}")
                return transform
            
            except Exception as e:
                self.get_logger().error(f"Failed to get transform: {str(e)}")


    def speech_text(self, text):
        while not self.speech_client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for speech_text service...')
        
        request = SpeechText.Request()
        request.text = text
        future = self.speech_client_.call_async(request)
        rclpy.spin_until_future_complete(future)
        if future.result() is not None:
            response = future.result()
            if response.result:
                self.get_logger().info('Speech synthesis successful')
            else:
                self.get_logger().error('Speech synthesis failed')
        else:
            self.get_logger().error(f'Service call failed: {future.exception()}')
    
def main():
    rclpy.init()
    patrol = PatrolNode()
    patrol.speech_text("正在准备初始化位置")
    patrol.init_robot_pose()
    patrol.speech_text("初始化位置完成")


    while rclpy.ok():
        patrol_points = patrol.get_target_point()
        for point in patrol_points:
            x,y,yaw = point[0], point[1], point[2]
            target_pose = patrol.get_pose_by_xyyaw(x, y, yaw)
            patrol.speech_text(f"正在前往巡逻点，坐标：{x}, {y}，朝向：{yaw}")
            patrol.nav_to_pose(target_pose)

    rclpy.shutdown()