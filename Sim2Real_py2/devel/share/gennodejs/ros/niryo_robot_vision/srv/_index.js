
"use strict";

let ObjDetection = require('./ObjDetection.js')
let TakePicture = require('./TakePicture.js')
let Visualization = require('./Visualization.js')
let DebugColorDetection = require('./DebugColorDetection.js')
let DebugMarkers = require('./DebugMarkers.js')
let SetImageParameter = require('./SetImageParameter.js')

module.exports = {
  ObjDetection: ObjDetection,
  TakePicture: TakePicture,
  Visualization: Visualization,
  DebugColorDetection: DebugColorDetection,
  DebugMarkers: DebugMarkers,
  SetImageParameter: SetImageParameter,
};
