// Part of the APK.audio project — http://APK.audio — made by Anthony Kuzub
// MIT Licence. Free, for everyone, for ever. Full text in LICENSE at the root.
// Aggregates every icon module into a single ordered list.
// Each icon lives in its own file (e.g. ./resistor.js) and exports a default
// object: { name, category, svg }.
import switchClosed from './switch-closed.js';
import switchOpen from './switch-open.js';
import selector from './selector.js';
import selected from './selected.js';
import cell from './cell.js';
import battery from './battery.js';
import acSource from './ac-source.js';
import voltageSource from './voltage-source.js';
import currentSource from './current-source.js';
import resistor from './resistor.js';
import capacitor from './capacitor.js';
import inductor from './inductor.js';
import wire from './wire.js';
import fuse from './fuse.js';
import breaker from './breaker.js';
import variableResistor from './variable-resistor.js';
import potentiometer from './potentiometer.js';
import thermistor from './thermistor.js';
import ammeter from './ammeter.js';
import voltmeter from './voltmeter.js';
import scopemeter from './scopemeter.js';
import wattmeter from './wattmeter.js';
import motor from './motor.js';
import diode from './diode.js';
import led from './led.js';
import zener from './zener.js';
import ldr from './ldr.js';
import ground from './ground.js';
import buzzer from './buzzer.js';
import loudspeaker from './loudspeaker.js';
import lamp from './lamp.js';
import transistor from './transistor.js';
import transistorP from './transistorp.js';
import fet from './fet.js';
import fetP from './fetp.js';
import jfetN from './jfetn.js';
import jfetP from './jfetp.js';
import opamp from './opamp.js';
import antenna from './antenna.js';
import transformer from './transformer.js';
import and from './and.js';
import or from './or.js';
import not from './not.js';
import nand from './nand.js';
import nor from './nor.js';
import xor from './xor.js';
import xnor from './xnor.js';

// ---- Colour variants ----
import acC from './ac-color.js';
import ammeterC from './ammeter-color.js';
import voltmeterC from './voltmeter-color.js';
import scopemeterC from './scopemeter-color.js';
import motorC from './motor-color.js';
import wattmeterC from './wattmeter-color.js';
import antennaC from './antenna-color.js';
import buzzerC from './buzzer-color.js';
import cellC from './cell-color.js';
import cellsC from './cells-color.js';
import currentC from './current-color.js';
import transistorNC from './transistorn-color.js';
import transistorPC from './transistorp-color.js';
import groundC from './ground-color.js';
import jfetNC from './jfetn-color.js';
import jfetPC from './jfetp-color.js';
import lampC from './lamp-color.js';
import ledC from './led-color.js';
import opampC from './opamp-color.js';
import potentiometerC from './potentiometer-color.js';
import rheostatC from './rheostat-color.js';
import selectedC from './selected-color.js';
import selectorC from './selector-color.js';
import switchClosedC from './switch-closed-color.js';
import thermistorC from './thermistor-color.js';
import transformerC from './transformer-color.js';
import voltageC from './voltage-color.js';
import andC from './and-color.js';
import orC from './or-color.js';
import notC from './not-color.js';
import nandC from './nand-color.js';
import norC from './nor-color.js';
import xorC from './xor-color.js';
import xnorC from './xnor-color.js';

export default [
  switchClosed, switchOpen, selector, selected, cell, battery, acSource, voltageSource, currentSource, resistor, capacitor, inductor, wire,
  fuse, breaker, variableResistor, potentiometer, thermistor, ammeter, voltmeter, scopemeter, wattmeter, motor, diode, led, zener, ldr,
  ground, buzzer, loudspeaker, lamp, transistor, transistorP, fet, fetP, jfetN, jfetP, opamp, antenna, transformer,
  and, or, not, nand, nor, xor, xnor,
  // ---- Colour variants ----
  acC, voltageC, currentC, cellC, cellsC, switchClosedC, selectorC, selectedC,
  rheostatC, potentiometerC, thermistorC, ammeterC, voltmeterC, scopemeterC, wattmeterC, motorC,
  ledC, groundC, buzzerC, lampC, transistorNC, transistorPC, jfetNC, jfetPC,
  opampC, antennaC, transformerC,
  andC, orC, notC, nandC, norC, xorC, xnorC
];
