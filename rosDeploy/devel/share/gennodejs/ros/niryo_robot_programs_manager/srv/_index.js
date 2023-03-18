
"use strict";

let GetProgram = require('./GetProgram.js')
let GetProgramAutorunInfos = require('./GetProgramAutorunInfos.js')
let GetProgramList = require('./GetProgramList.js')
let ManageProgram = require('./ManageProgram.js')
let SetProgramAutorun = require('./SetProgramAutorun.js')
let ExecuteProgram = require('./ExecuteProgram.js')

module.exports = {
  GetProgram: GetProgram,
  GetProgramAutorunInfos: GetProgramAutorunInfos,
  GetProgramList: GetProgramList,
  ManageProgram: ManageProgram,
  SetProgramAutorun: SetProgramAutorun,
  ExecuteProgram: ExecuteProgram,
};
