// Generated by gencpp from file tools_interface/Tool.msg
// DO NOT EDIT!


#ifndef TOOLS_INTERFACE_MESSAGE_TOOL_H
#define TOOLS_INTERFACE_MESSAGE_TOOL_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace tools_interface
{
template <class ContainerAllocator>
struct Tool_
{
  typedef Tool_<ContainerAllocator> Type;

  Tool_()
    : id(0)
    , motor_type(0)
    , position(0)
    , state(0)  {
    }
  Tool_(const ContainerAllocator& _alloc)
    : id(0)
    , motor_type(0)
    , position(0)
    , state(0)  {
  (void)_alloc;
    }



   typedef int8_t _id_type;
  _id_type id;

   typedef int8_t _motor_type_type;
  _motor_type_type motor_type;

   typedef int16_t _position_type;
  _position_type position;

   typedef int8_t _state_type;
  _state_type state;



// reducing the odds to have name collisions with Windows.h 
#if defined(_WIN32) && defined(NO_MOTOR)
  #undef NO_MOTOR
#endif
#if defined(_WIN32) && defined(STEPPER)
  #undef STEPPER
#endif
#if defined(_WIN32) && defined(XL430)
  #undef XL430
#endif
#if defined(_WIN32) && defined(XL320)
  #undef XL320
#endif
#if defined(_WIN32) && defined(XL330)
  #undef XL330
#endif
#if defined(_WIN32) && defined(XC430)
  #undef XC430
#endif
#if defined(_WIN32) && defined(XM430)
  #undef XM430
#endif
#if defined(_WIN32) && defined(FAKE_DXL_MOTOR)
  #undef FAKE_DXL_MOTOR
#endif
#if defined(_WIN32) && defined(TOOL_STATE_PING_OK)
  #undef TOOL_STATE_PING_OK
#endif
#if defined(_WIN32) && defined(TOOL_STATE_PING_ERROR)
  #undef TOOL_STATE_PING_ERROR
#endif
#if defined(_WIN32) && defined(TOOL_STATE_WRONG_ID)
  #undef TOOL_STATE_WRONG_ID
#endif
#if defined(_WIN32) && defined(TOOL_STATE_TIMEOUT)
  #undef TOOL_STATE_TIMEOUT
#endif
#if defined(_WIN32) && defined(GRIPPER_STATE_OPEN)
  #undef GRIPPER_STATE_OPEN
#endif
#if defined(_WIN32) && defined(GRIPPER_STATE_CLOSE)
  #undef GRIPPER_STATE_CLOSE
#endif
#if defined(_WIN32) && defined(VACUUM_PUMP_STATE_PULLED)
  #undef VACUUM_PUMP_STATE_PULLED
#endif
#if defined(_WIN32) && defined(VACUUM_PUMP_STATE_PUSHED)
  #undef VACUUM_PUMP_STATE_PUSHED
#endif

  enum {
    NO_MOTOR = 0,
    STEPPER = 1,
    XL430 = 2,
    XL320 = 3,
    XL330 = 4,
    XC430 = 5,
    XM430 = 6,
    FAKE_DXL_MOTOR = 20,
    TOOL_STATE_PING_OK = 1,
    TOOL_STATE_PING_ERROR = 2,
    TOOL_STATE_WRONG_ID = 3,
    TOOL_STATE_TIMEOUT = 4,
    GRIPPER_STATE_OPEN = 16,
    GRIPPER_STATE_CLOSE = 17,
    VACUUM_PUMP_STATE_PULLED = 32,
    VACUUM_PUMP_STATE_PUSHED = 33,
  };


  typedef boost::shared_ptr< ::tools_interface::Tool_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::tools_interface::Tool_<ContainerAllocator> const> ConstPtr;

}; // struct Tool_

typedef ::tools_interface::Tool_<std::allocator<void> > Tool;

typedef boost::shared_ptr< ::tools_interface::Tool > ToolPtr;
typedef boost::shared_ptr< ::tools_interface::Tool const> ToolConstPtr;

// constants requiring out of line definition

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   

   



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::tools_interface::Tool_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::tools_interface::Tool_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::tools_interface::Tool_<ContainerAllocator1> & lhs, const ::tools_interface::Tool_<ContainerAllocator2> & rhs)
{
  return lhs.id == rhs.id &&
    lhs.motor_type == rhs.motor_type &&
    lhs.position == rhs.position &&
    lhs.state == rhs.state;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::tools_interface::Tool_<ContainerAllocator1> & lhs, const ::tools_interface::Tool_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace tools_interface

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::tools_interface::Tool_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::tools_interface::Tool_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::tools_interface::Tool_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::tools_interface::Tool_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::tools_interface::Tool_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::tools_interface::Tool_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::tools_interface::Tool_<ContainerAllocator> >
{
  static const char* value()
  {
    return "830c50232809d26b16dfe357c84d738a";
  }

  static const char* value(const ::tools_interface::Tool_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x830c50232809d26bULL;
  static const uint64_t static_value2 = 0x16dfe357c84d738aULL;
};

template<class ContainerAllocator>
struct DataType< ::tools_interface::Tool_<ContainerAllocator> >
{
  static const char* value()
  {
    return "tools_interface/Tool";
  }

  static const char* value(const ::tools_interface::Tool_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::tools_interface::Tool_<ContainerAllocator> >
{
  static const char* value()
  {
    return "int8 id\n"
"\n"
"int8 NO_MOTOR = 0\n"
"int8 STEPPER = 1\n"
"int8 XL430 = 2\n"
"int8 XL320 = 3\n"
"int8 XL330 = 4\n"
"int8 XC430 = 5\n"
"int8 XM430 = 6\n"
"int8 FAKE_DXL_MOTOR = 20\n"
"\n"
"int8 motor_type\n"
"\n"
"int16 position\n"
"\n"
"int8 TOOL_STATE_PING_OK       = 1\n"
"int8 TOOL_STATE_PING_ERROR    = 2\n"
"int8 TOOL_STATE_WRONG_ID      = 3\n"
"int8 TOOL_STATE_TIMEOUT       = 4\n"
"\n"
"int8 GRIPPER_STATE_OPEN       = 16\n"
"int8 GRIPPER_STATE_CLOSE      = 17\n"
"\n"
"int8 VACUUM_PUMP_STATE_PULLED = 32\n"
"int8 VACUUM_PUMP_STATE_PUSHED = 33\n"
"\n"
"int8 state\n"
;
  }

  static const char* value(const ::tools_interface::Tool_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::tools_interface::Tool_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.id);
      stream.next(m.motor_type);
      stream.next(m.position);
      stream.next(m.state);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct Tool_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::tools_interface::Tool_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::tools_interface::Tool_<ContainerAllocator>& v)
  {
    s << indent << "id: ";
    Printer<int8_t>::stream(s, indent + "  ", v.id);
    s << indent << "motor_type: ";
    Printer<int8_t>::stream(s, indent + "  ", v.motor_type);
    s << indent << "position: ";
    Printer<int16_t>::stream(s, indent + "  ", v.position);
    s << indent << "state: ";
    Printer<int8_t>::stream(s, indent + "  ", v.state);
  }
};

} // namespace message_operations
} // namespace ros

#endif // TOOLS_INTERFACE_MESSAGE_TOOL_H