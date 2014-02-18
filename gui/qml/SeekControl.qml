import QtQuick 2.0

Item {
    id: seekControl
    height: 45
    property int duration: 0
    property int playPosition: 0
    property int seekPosition: 0
    property bool enabled: true
    property bool seeking: false

//    Rectangle {
//        id: background
//        anchors.fill: parent
//        color: "yellow"
//        opacity: 0.3
//        height: 15
//    }

    Rectangle {
        id: progressBar
        anchors { left: parent.left; top: parent.top; right: parent.right}
        width: seekControl.duration == 0 ? 0 : background.width * seekControl.playPosition / seekControl.duration
        color: "gray"
        opacity: 0.5
        height: 12
        MouseArea {
            anchors.fill: parent
            onClicked: {
                seekControl.seekPosition = mouseX*seekControl.duration/width
            }
        }
    }
    Rectangle {
        id: progress
        anchors { left: parent.left; top: parent.top; right: progressHandle.right}
        width: seekControl.duration == 0 ? 0 : background.width * seekControl.playPosition / seekControl.duration
        color: "orange"
        opacity: 0.7
        height: 12

    }

    Text {
        anchors { left: parent.left; top: progressBar.bottom; topMargin: 7}
        font { family: "Nokia Sans S60"; pixelSize: 14 }
        horizontalAlignment: Text.AlignLeft
        verticalAlignment: Text.AlignVCenter
        color: "white"
        smooth: true
        text: formatTime(playPosition)
    }

    Text {
        anchors { right: parent.right; top: progressBar.bottom; topMargin: 7}
        font { family: "Nokia Sans S60"; pixelSize: 14 }
        horizontalAlignment: Text.AlignRight
        verticalAlignment: Text.AlignVCenter
        color: "white"
        smooth: true
        text: formatTime(duration)
    }

    Rectangle {
        id: progressHandle
        height: 12
        width: 12
        color: mouseArea.pressed ? "gray" : "white"
        anchors.verticalCenter: progressBar.verticalCenter
        x: seekControl.duration == 0 ? 0 : seekControl.playPosition / seekControl.duration * (seekControl.width - 12)

        MouseArea {
            id: mouseArea
            anchors { horizontalCenter: parent.horizontalCenter; bottom: parent.bottom }
            height: 12+16
            width: height
            enabled: seekControl.enabled
            drag {
                target: progressHandle
                axis: Drag.XAxis
                minimumX: 0
                maximumX: (seekControl.width - 12)
            }
            onPressed: {
                seekControl.seeking = true;
            }
            onCanceled: {
                seekControl.seekPosition = progressHandle.x * seekControl.duration / (seekControl.width - 12)
                seekControl.seeking = false
            }
            onReleased: {
                seekControl.seekPosition = progressHandle.x * seekControl.duration / (seekControl.width - 12)
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
            seekControl.seekPosition = progressHandle.x*seekControl.duration/(seekControl.width - 12)
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
