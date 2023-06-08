from ctypes import *
import time
import thread

# Type redefine!
BOOL = c_int
DWORD = c_ulong
HANDLE = c_void_p
UINT = c_uint
CHAR = c_char_p
USHORT = c_ushort
LONG = c_long
INT = c_int


#####################################################################################################################################################################################

# Rotation Motor Class


class MaxonMotor(object):
    BOOL = c_int
    DWORD = c_ulong
    HANDLE = c_void_p
    UINT = c_uint
    CHAR = c_char_p
    USHORT = c_ushort
    LONG = c_long
    INT = c_int

    """rotation motor"""

    def __init__(self, RMNodeId, pDeviceName, pProtocolStackName, pInterfaceName, pPortName, lBaudrate):
        # Type redefine!

        self.RMNodeId = USHORT(RMNodeId)
        self.pDeviceName = CHAR(pDeviceName)
        self.pProtocolStackName = CHAR(pProtocolStackName)
        self.pInterfaceName = CHAR(pInterfaceName)
        self.pPortName = CHAR(pPortName)
        self.lBaudrate = UINT(lBaudrate)
        self.RMHandle = HANDLE(0)
        self.errorCode = UINT(0)
        self.lTimeout = UINT(0)
        self.current = LONG(0)

        # self.relativePosition = LONG(relativePosition)
        self.rmPosition = INT(0)
        self.rmVelosity = INT(0)

        self.rotationMotor = cdll.LoadLibrary("libEposCmd.so")

        # Open Device
        self.OpenDevice = self.rotationMotor.VCS_OpenDevice
        self.OpenDevice.argtypes = [CHAR, CHAR, CHAR, CHAR, POINTER(UINT)]
        self.OpenDevice.restype = HANDLE

        # Communication Info
        self.GetProtocolStackSettings = self.rotationMotor.VCS_GetProtocolStackSettings
        self.GetProtocolStackSettings.argtypes = [HANDLE, POINTER(UINT), POINTER(UINT), POINTER(UINT)]
        self.GetProtocolStackSettings.restype = BOOL

        self.SetProtocolStackSettings = self.rotationMotor.VCS_SetProtocolStackSettings
        self.SetProtocolStackSettings.argtypes = [HANDLE, USHORT, UINT, POINTER(UINT)]
        self.SetProtocolStackSettings.restype = BOOL

        ##############################Opration mode
        self.SetOperationMode = self.rotationMotor.VCS_SetOperationMode
        self.SetOperationMode.argtypes = [HANDLE, USHORT, CHAR, POINTER(UINT)]
        self.SetOperationMode.restype = BOOL

        # Enable Motor
        self.SetEnableState = self.rotationMotor.VCS_SetEnableState
        self.SetEnableState.argtypes = [HANDLE, USHORT, POINTER(UINT)]
        self.SetEnableState.restype = BOOL

        self.GetEnableState = self.rotationMotor.VCS_GetEnableState
        self.GetEnableState.argtypes = [HANDLE, USHORT, POINTER(BOOL), POINTER(UINT)]
        self.GetEnableState.restype = BOOL

        self.SetDisableState = self.rotationMotor.VCS_SetDisableState
        self.SetDisableState.argtypes = [HANDLE, USHORT, POINTER(UINT)]
        self.SetDisableState.restype = BOOL

        # Clear Fault
        self.GetFaultState = self.rotationMotor.VCS_GetFaultState
        self.GetFaultState.argtypes = [HANDLE, USHORT, POINTER(BOOL), POINTER(UINT)]
        self.GetFaultState.restype = BOOL

        self.ClearFault = self.rotationMotor.VCS_ClearFault
        self.ClearFault.argtypes = [HANDLE, USHORT, POINTER(UINT)]
        self.ClearFault.restype = BOOL

        # Velocity Mode
        self.MoveWithVelocity = self.rotationMotor.VCS_MoveWithVelocity
        self.MoveWithVelocity.argtypes = [HANDLE, USHORT, LONG, POINTER(UINT)]
        self.MoveWithVelocity.restype = BOOL

        self.ActivateProfileVelocityMode = self.rotationMotor.VCS_ActivateProfileVelocityMode
        self.ActivateProfileVelocityMode.argtypes = [HANDLE, USHORT, POINTER(UINT)]
        self.ActivateProfileVelocityMode.restype = BOOL

        self.SetVelocityProfile = self.rotationMotor.VCS_SetVelocityProfile
        self.SetVelocityProfile.argtypes = [HANDLE, USHORT, UINT, UINT, POINTER(UINT)]
        self.SetVelocityProfile.restype = BOOL

        self.HaltVelocityMovement = self.rotationMotor.VCS_HaltVelocityMovement
        self.HaltVelocityMovement.argtypes = [HANDLE, USHORT, POINTER(UINT)]
        self.HaltVelocityMovement.restype = BOOL

        self.GetVelocityProfile = self.rotationMotor.VCS_GetVelocityProfile
        self.GetVelocityProfile.argtypes = [HANDLE, USHORT, POINTER(UINT), POINTER(UINT), POINTER(UINT)]
        self.GetVelocityProfile.restype = BOOL

        # Position Mode
        self.ActivateProfilePositionMode = self.rotationMotor.VCS_ActivateProfilePositionMode
        self.ActivateProfilePositionMode.argtypes = [HANDLE, USHORT, POINTER(DWORD)]
        self.ActivateProfilePositionMode.restype = BOOL

        self.SetPositionProfile = self.rotationMotor.VCS_SetPositionProfile
        self.SetPositionProfile.argtypes = [HANDLE, USHORT, UINT, UINT, UINT, POINTER(DWORD)]
        self.SetPositionProfile.restype = BOOL

        self.MoveToPosition = self.rotationMotor.VCS_MoveToPosition
        self.MoveToPosition.argtypes = [HANDLE, USHORT, LONG, INT, INT, POINTER(DWORD)]
        self.MoveToPosition.restype = BOOL

        self.HaltPositionMovement = self.rotationMotor.VCS_HaltPositionMovement
        self.HaltPositionMovement.argtypes = [HANDLE, USHORT, POINTER(DWORD)]
        self.HaltPositionMovement.restype = BOOL

        # Max Speed
        self.SetMaxProfileVelocity = self.rotationMotor.VCS_SetMaxProfileVelocity
        self.SetMaxProfileVelocity.argtypes = [HANDLE, USHORT, UINT, POINTER(UINT)]
        self.SetMaxProfileVelocity.restype = BOOL

        # Motor Speed and Position Info
        self.GetPosition = self.rotationMotor.VCS_GetPositionIs
        self.GetPosition.argtypes = [HANDLE, USHORT, POINTER(INT), POINTER(UINT)]
        self.GetPosition.restype = BOOL

        self.GetVelocity = self.rotationMotor.VCS_GetVelocityIs
        self.GetVelocity.argtypes = [HANDLE, USHORT, POINTER(INT), POINTER(UINT)]
        self.GetVelocity.restype = BOOL
        
        self.GetCurrent = self.rotationMotor.VCS_GetCurrentIs
        self.GetCurrent.argtypes = [HANDLE, USHORT, POINTER(INT), POINTER(UINT)]
        self.GetCurrent.restype = BOOL

        # Close Device
        self.CloseDevice = self.rotationMotor.VCS_CloseDevice
        self.CloseDevice.argtypes = [HANDLE, POINTER(UINT)]
        self.CloseDevice.restype = BOOL

        # Close All Device
        self.CloseAllDevices = self.rotationMotor.VCS_CloseAllDevices
        self.CloseAllDevices.argtypes = [POINTER(UINT)]
        self.CloseAllDevices.restype = BOOL

        self.open_device()

    # Open Device
    def open_device(self):
        Result = 0
        oIsFault = BOOL(0)
        oIsEnabled = BOOL(0)

        print "Open Device-----"
        self.RMHandle = self.OpenDevice(self.pDeviceName, self.pProtocolStackName, self.pInterfaceName, self.pPortName,
                                        byref(self.errorCode))
        print self.RMHandle, self.errorCode.value

        self.ClearFault(self.RMHandle, self.RMNodeId, byref(self.errorCode))
        self.SetEnableState(self.RMHandle, self.RMNodeId, byref(self.errorCode))
        return Result

    # Position Mode
    def rm_move_to_position(self, positionModeSpeed, targetRelativePosition):
        Result = 0
        if self.SetOperationMode(self.RMHandle, self.RMNodeId, "1", byref(self.errorCode)) != BOOL(0):
            if self.ActivateProfilePositionMode(self.RMHandle, self.RMNodeId, byref(self.errorCode)) != BOOL(0):
                if self.SetPositionProfile(self.RMHandle, self.RMNodeId, UINT(positionModeSpeed), 1000, 1000,
                                           byref(self.errorCode)) != BOOL(0):
                    if self.MoveToPosition(self.RMHandle, self.RMNodeId, LONG(targetRelativePosition), INT(0), INT(1),
                                           byref(self.errorCode)) != BOOL(0):
                        Result = 1

        return Result

    # Close Device
    def close_device(self):
        Result = 0
        if self.CloseDevice(self.RMHandle, byref(self.errorCode)) != BOOL(0):
            Result = 1
        return Result

    # Velocity  Mode
    def rm_move(self, TargetVelocity):
        Result = 0
        positionModeAcceleration = UINT(1000)
        positionModeDeceleration = UINT(1000)
        if self.SetOperationMode(self.RMHandle, self.RMNodeId, "3", byref(self.errorCode)) != BOOL(0):
            if self.ActivateProfileVelocityMode(self.RMHandle, self.RMNodeId, byref(self.errorCode)) != BOOL(0):
                # print "ActivateProfileVelocityMode is successful"
                if self.SetVelocityProfile(self.RMHandle, self.RMNodeId, positionModeAcceleration,
                                           positionModeDeceleration, byref(self.errorCode)) != BOOL(0):
                    # print "SetVelocityProfile is successful"
                    if self.MoveWithVelocity(self.RMHandle, self.RMNodeId, LONG(TargetVelocity),
                                             byref(self.errorCode)) != BOOL(0):
                        print "MoveWithVelocity"
                        # time.sleep(5)
                        Result = 1

        return Result

    ##################################################################
    def rm_disable(self):
        Result = 0
        if self.SetDisableState(self.RMHandle, self.RMNodeId, byref(self.errorCode)) != BOOL(0):
            Result = 1

        return Result
    ###################
    def get_current(self):
        Result = 0
        if self.GetCurrent(self.RMHandle, self.RMNodeId, self.current,byref(self.errorCode))!= BOOL(0):
            Result = self.current
            #print self.current
            
        return Result


#####################################################################################################################################################################################
#guidewireRotateMotor1 = MaxonMotor(1, "EPOS2", "MAXON SERIAL V2", "USB", "USB0", 1000000)
#time.sleep(1)
#guidewireRotateMotor1.rm_move(150)
#time.sleep(5)
#guidewireRotateMotor1.rm_move(-150)
#time.sleep(5)
#guidewireRotateMotor1.rm_disable()
#guidewireRotateMotor1.close_device()
