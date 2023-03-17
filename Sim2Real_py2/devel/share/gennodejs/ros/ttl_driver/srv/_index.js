
"use strict";

let ReadPIDValue = require('./ReadPIDValue.js')
let ReadCustomValue = require('./ReadCustomValue.js')
let WriteCustomValue = require('./WriteCustomValue.js')
let WritePIDValue = require('./WritePIDValue.js')
let WriteVelocityProfile = require('./WriteVelocityProfile.js')
let ReadVelocityProfile = require('./ReadVelocityProfile.js')

module.exports = {
  ReadPIDValue: ReadPIDValue,
  ReadCustomValue: ReadCustomValue,
  WriteCustomValue: WriteCustomValue,
  WritePIDValue: WritePIDValue,
  WriteVelocityProfile: WriteVelocityProfile,
  ReadVelocityProfile: ReadVelocityProfile,
};
