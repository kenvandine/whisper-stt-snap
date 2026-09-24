*** Settings ***
Documentation    Test cases for whisper-stt snap
Resource         kvm.resource


*** Test Cases ***
Whisper Stt Launches And Renders
    [Documentation]    Verify whisper-stt snap launches and renders a UI on Mir
    [Tags]    smoke    yarf:certification_status: blocker
    Log Screenshot
