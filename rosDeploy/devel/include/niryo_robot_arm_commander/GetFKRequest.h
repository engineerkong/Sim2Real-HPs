// Generated by gencpp from file niryo_robot_arm_commander/GetFKRequest.msg
// DO NOT EDIT!


#ifndef NIRYO_ROBOT_ARM_COMMANDER_MESSAGE_GETFKREQUEST_H
#define NIRYO_ROBOT_ARM_COMMANDER_MESSAGE_GETFKREQUEST_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace niryo_robot_arm_commander
{
template <class ContainerAllocator>
struct GetFKRequest_
{
  typedef GetFKRequest_<ContainerAllocator> Type;

  GetFKRequest_()
    : joints()  {
    }
  GetFKRequest_(const ContainerAllocator& _alloc)
    : joints(_alloc)  {
  (void)_alloc;
    }



   typedef std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> _joints_type;
  _joints_type joints;





  typedef boost::shared_ptr< ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator> const> ConstPtr;

}; // struct GetFKRequest_

typedef ::niryo_robot_arm_commander::GetFKRequest_<std::allocator<void> > GetFKRequest;

typedef boost::shared_ptr< ::niryo_robot_arm_commander::GetFKRequest > GetFKRequestPtr;
typedef boost::shared_ptr< ::niryo_robot_arm_commander::GetFKRequest const> GetFKRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator1> & lhs, const ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator2> & rhs)
{
  return lhs.joints == rhs.joints;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator1> & lhs, const ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace niryo_robot_arm_commander

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "e2a0e438b445b98def0f0ba6a2a85f58";
  }

  static const char* value(const ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xe2a0e438b445b98dULL;
  static const uint64_t static_value2 = 0xef0f0ba6a2a85f58ULL;
};

template<class ContainerAllocator>
struct DataType< ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "niryo_robot_arm_commander/GetFKRequest";
  }

  static const char* value(const ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float32[] joints\n"
;
  }

  static const char* value(const ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.joints);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct GetFKRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::niryo_robot_arm_commander::GetFKRequest_<ContainerAllocator>& v)
  {
    s << indent << "joints[]" << std::endl;
    for (size_t i = 0; i < v.joints.size(); ++i)
    {
      s << indent << "  joints[" << i << "]: ";
      Printer<float>::stream(s, indent + "  ", v.joints[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // NIRYO_ROBOT_ARM_COMMANDER_MESSAGE_GETFKREQUEST_H