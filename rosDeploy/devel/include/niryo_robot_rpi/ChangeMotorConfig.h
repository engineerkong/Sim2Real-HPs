// Generated by gencpp from file niryo_robot_rpi/ChangeMotorConfig.msg
// DO NOT EDIT!


#ifndef NIRYO_ROBOT_RPI_MESSAGE_CHANGEMOTORCONFIG_H
#define NIRYO_ROBOT_RPI_MESSAGE_CHANGEMOTORCONFIG_H

#include <ros/service_traits.h>


#include <niryo_robot_rpi/ChangeMotorConfigRequest.h>
#include <niryo_robot_rpi/ChangeMotorConfigResponse.h>


namespace niryo_robot_rpi
{

struct ChangeMotorConfig
{

typedef ChangeMotorConfigRequest Request;
typedef ChangeMotorConfigResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct ChangeMotorConfig
} // namespace niryo_robot_rpi


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::niryo_robot_rpi::ChangeMotorConfig > {
  static const char* value()
  {
    return "4656a66d9c8c003dc0f8aa40d5770162";
  }

  static const char* value(const ::niryo_robot_rpi::ChangeMotorConfig&) { return value(); }
};

template<>
struct DataType< ::niryo_robot_rpi::ChangeMotorConfig > {
  static const char* value()
  {
    return "niryo_robot_rpi/ChangeMotorConfig";
  }

  static const char* value(const ::niryo_robot_rpi::ChangeMotorConfig&) { return value(); }
};


// service_traits::MD5Sum< ::niryo_robot_rpi::ChangeMotorConfigRequest> should match
// service_traits::MD5Sum< ::niryo_robot_rpi::ChangeMotorConfig >
template<>
struct MD5Sum< ::niryo_robot_rpi::ChangeMotorConfigRequest>
{
  static const char* value()
  {
    return MD5Sum< ::niryo_robot_rpi::ChangeMotorConfig >::value();
  }
  static const char* value(const ::niryo_robot_rpi::ChangeMotorConfigRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::niryo_robot_rpi::ChangeMotorConfigRequest> should match
// service_traits::DataType< ::niryo_robot_rpi::ChangeMotorConfig >
template<>
struct DataType< ::niryo_robot_rpi::ChangeMotorConfigRequest>
{
  static const char* value()
  {
    return DataType< ::niryo_robot_rpi::ChangeMotorConfig >::value();
  }
  static const char* value(const ::niryo_robot_rpi::ChangeMotorConfigRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::niryo_robot_rpi::ChangeMotorConfigResponse> should match
// service_traits::MD5Sum< ::niryo_robot_rpi::ChangeMotorConfig >
template<>
struct MD5Sum< ::niryo_robot_rpi::ChangeMotorConfigResponse>
{
  static const char* value()
  {
    return MD5Sum< ::niryo_robot_rpi::ChangeMotorConfig >::value();
  }
  static const char* value(const ::niryo_robot_rpi::ChangeMotorConfigResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::niryo_robot_rpi::ChangeMotorConfigResponse> should match
// service_traits::DataType< ::niryo_robot_rpi::ChangeMotorConfig >
template<>
struct DataType< ::niryo_robot_rpi::ChangeMotorConfigResponse>
{
  static const char* value()
  {
    return DataType< ::niryo_robot_rpi::ChangeMotorConfig >::value();
  }
  static const char* value(const ::niryo_robot_rpi::ChangeMotorConfigResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // NIRYO_ROBOT_RPI_MESSAGE_CHANGEMOTORCONFIG_H