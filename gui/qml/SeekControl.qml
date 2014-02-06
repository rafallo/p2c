import QtQuick 2.0

Item {
    id: seekControl
    height: 46
    property int duration: 0
    property int playPosition: 0
    property int seekPosition: 0
    property bool enabled: true
    property bool seeking: false

    Rectangle {
        id: background
        anchors.fill: parent
        color: "black"
        opacity: 0.3
    }

    Rectangle {
        id: progressBar
        anchors { left: parent.left; top: parent.top; bottom: parent.bottom }
        width: seekControl.duration == 0 ? 0 : background.width * seekControl.playPosition / seekControl.duration
        color: "red"
        opacity: 0.7
    }

    Text {
        width: 90
        anchors { left: parent.left; top: parent.top; bottom: parent.bottom; leftMargin: 10 }
        font { family: "Nokia Sans S60"; pixelSize: 24 }
        horizontalAlignment: Text.AlignLeft
        verticalAlignment: Text.AlignVCenter
        color: "white"
        smooth: true
        text: formatTime(playPosition)
    }

    Text {
        width: 90
        anchors { right: parent.right; top: parent.top; bottom: parent.bottom; rightMargin: 10 }
        font { family: "Nokia Sans S60"; pixelSize: 24 }
        horizontalAlignment: Text.AlignRight
        verticalAlignment: Text.AlignVCenter
        color: "white"
        smooth: true
        text: formatTime(duration)
    }

    Image {
        id: progressHandle
        height: 46
        width: 10
        source: mouseArea.pressed ? "images/progress_handle_pressed.svg" : "images/progress_handle.svg"
        anchors.verticalCenter: progressBar.verticalCenter
        x: seekControl.duration == 0 ? 0 : seekControl.playPosition / seekControl.duration * 630

        MouseArea {
            id: mouseArea
            anchors { horizontalCenter: parent.horizontalCenter; bottom: parent.bottom }
            height: 46+16
            width: height
            enabled: seekControl.enabled
            drag {
                target: progressHandle
                axis: Drag.XAxis
                minimumX: 0
                maximumX: 631
            }
            onPressed: {
                seekControl.seeking = true;
            }
            onCanceled: {
                seekControl.seekPosition = progressHandle.x * seekControl.duration / 630
                seekControl.seeking = false
            }
            onReleased: {
                seekControl.seekPosition = progressHandle.x * seekControl.duration / 630
                seekControl.seeking = false
                mouse.accepted = true
            }
        }
    }

    Timer { // Update position also while user is dragging the progress handle
        id: seekTimer
        repeat: true
        interval: 300
        running: seekControl.seeking
        onTriggered: {
            seekControl.seekPosition = progressHandle.x*seekControl.duration/630
        }
    }

    function formatTime(timeInMs) {
        if (!timeInMs || timeInMs <= 0) return "0:00"
        var seconds = timeInMs / 1000;
        var minutes = Math.floor(seconds / 60)
        seconds = Math.floor(seconds % 60)
        if (seconds < 10) seconds = "0" + seconds;
        return minutes + ":" + seconds
    }
}
