// Generated by gencpp from file end_effector_interface/SetEEDigitalOut.msg
// DO NOT EDIT!


#ifndef END_EFFECTOR_INTERFACE_MESSAGE_SETEEDIGITALOUT_H
#define END_EFFECTOR_INTERFACE_MESSAGE_SETEEDIGITALOUT_H

#include <ros/service_traits.h>


#include <end_effector_interface/SetEEDigitalOutRequest.h>
#include <end_effector_interface/SetEEDigitalOutResponse.h>


namespace end_effector_interface
{

struct SetEEDigitalOut
{

typedef SetEEDigitalOutRequest Request;
typedef SetEEDigitalOutResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct SetEEDigitalOut
} // namespace end_effector_interface


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::end_effector_interface::SetEEDigitalOut > {
  static const char* value()
  {
    return "33ab7459542983349e0a81fbf65f814c";
  }

  static const char* value(const ::end_effector_interface::SetEEDigitalOut&) { return value(); }
};

template<>
struct DataType< ::end_effector_interface::SetEEDigitalOut > {
  static const char* value()
  {
    return "end_effector_interface/SetEEDigitalOut";
  }

  static const char* value(const ::end_effector_interface::SetEEDigitalOut&) { return value(); }
};


// service_traits::MD5Sum< ::end_effector_interface::SetEEDigitalOutRequest> should match
// service_traits::MD5Sum< ::end_effector_interface::SetEEDigitalOut >
template<>
struct MD5Sum< ::end_effector_interface::SetEEDigitalOutRequest>
{
  static const char* value()
  {
    return MD5Sum< ::end_effector_interface::SetEEDigitalOut >::value();
  }
  static const char* value(const ::end_effector_interface::SetEEDigitalOutRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::end_effector_interface::SetEEDigitalOutRequest> should match
// service_traits::DataType< ::end_effector_interface::SetEEDigitalOut >
template<>
struct DataType< ::end_effector_interface::SetEEDigitalOutRequest>
{
  static const char* value()
  {
    return DataType< ::end_effector_interface::SetEEDigitalOut >::value();
  }
  static const char* value(const ::end_effector_interface::SetEEDigitalOutRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::end_effector_interface::SetEEDigitalOutResponse> should match
// service_traits::MD5Sum< ::end_effector_interface::SetEEDigitalOut >
template<>
struct MD5Sum< ::end_effector_interface::SetEEDigitalOutResponse>
{
  static const char* value()
  {
    return MD5Sum< ::end_effector_interface::SetEEDigitalOut >::value();
  }
  static const char* value(const ::end_effector_interface::SetEEDigitalOutResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::end_effector_interface::SetEEDigitalOutResponse> should match
// service_traits::DataType< ::end_effector_interface::SetEEDigitalOut >
template<>
struct DataType< ::end_effector_interface::SetEEDigitalOutResponse>
{
  static const char* value()
  {
    return DataType< ::end_effector_interface::SetEEDigitalOut >::value();
  }
  static const char* value(const ::end_effector_interface::SetEEDigitalOutResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // END_EFFECTOR_INTERFACE_MESSAGE_SETEEDIGITALOUT_H