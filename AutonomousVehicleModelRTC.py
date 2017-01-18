#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file AutonomousVehicleModelRTC.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
import numpy as np

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
autonomousvehiclemodelrtc_spec = ["implementation_id", "AutonomousVehicleModelRTC", 
		 "type_name",         "AutonomousVehicleModelRTC", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "Tao Asato", 
		 "category",          "Category", 
		 "activity_type",     "UNIQUE", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class AutonomousVehicleModelRTC
# @brief ModuleDescription
# 
# 
class AutonomousVehicleModelRTC(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		targetVel_arg = [None] * ((len(RTC._d_TimedVelocity2D) - 4) / 2)
		self._d_targetVel = RTC.TimedVelocity2D(RTC.Time(0,0), RTC.Velocity2D(0.0,0.0,0.0))
		"""
		"""
		self._targetVelIn = OpenRTM_aist.InPort("targetVel", self._d_targetVel)
		currentPose_arg = [None] * ((len(RTC._d_TimedPose2D) - 4) / 2)
		self._d_currentPose = RTC.TimedPose2D(RTC.Time(0,0), RTC.Pose2D(RTC.Point2D(0.0,0.0), 0.0)
)
		"""
		"""
		self._currentPoseOut = OpenRTM_aist.OutPort("currentPose", self._d_currentPose)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		
		# Set InPort buffers
		self.addInPort("targetVel",self._targetVelIn)
		
		# Set OutPort buffers
		self.addOutPort("currentPose",self._currentPoseOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The activated action (Active state entry action)
	#	# former rtc_active_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	# 
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	def onActivated(self, ec_id):
		self._d_currentPose.data.heading = 0.0
		self._d_currentPose.data.position.x = 0.0
		self._d_currentPose.data.position.y = 0.0
	
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The deactivated action (Active state exit action)
	#	# former rtc_active_exit()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onDeactivated(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The execution action that is invoked periodically
	#	# former rtc_active_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	dt = 0
	oldTime = RTC.Time(0.0,0.0)
	def onExecute(self, ec_id):
		if self._targetVelIn.isNew():
			self._targetVelIn.read()
			dt = self._d_targetVel.tm - oldTime
			oldTime = self._d_targetVel.tm

			self._d_currentPose.data.heading = self._d_targetVel.data.va*dt + self._d_currentPose.heading
			self._d_currentPose.data.position.x = self._d_targetVel.data.vx*dt*np.cos(self._d_currentPose.heading) + self._d_currentPose.position.x
			self._d_currentPose.data.position.y = self._d_targetVel.data.vx*dt*np.sin(self._d_currentPose.heading) + self._d_currentPose.position.y

		self._currentPoseOut.write()
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def AutonomousVehicleModelRTCInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=autonomousvehiclemodelrtc_spec)
    manager.registerFactory(profile,
                            AutonomousVehicleModelRTC,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    AutonomousVehicleModelRTCInit(manager)

    # Create a component
    comp = manager.createComponent("AutonomousVehicleModelRTC")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

