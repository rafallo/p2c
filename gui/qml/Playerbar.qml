import QtQuick 2.0

Rectangle {
    width: playerArea.width
    height: 140
    color: "black"
    SeekControl {
        anchors {
            left: parent.left
            right: parent.right
            leftMargin: 40
            rightMargin: 40
            topMargin: 10
            top: parent.top
        }
        duration: mediaPlayer ? mediaPlayer.duration : 0
        playPosition: mediaPlayer ? mediaPlayer.position : 0
        onSeekPositionChanged: { mediaPlayer.seek(seekPosition); }
    }

    Row {
        anchors {
            bottom: parent.bottom
            right: parent.right
            rightMargin: 40
            bottomMargin: 30
        }
        spacing: 20
        Image {
            height: 40
            source: poster
            fillMode: Image.PreserveAspectFit
        }

        Text {
            font { family: "Nokia Sans S60"; pixelSize: 22 }
            text: title
            color: "white"
            anchors {
                verticalCenter: parent.verticalCenter
            }
        }

        Image {
            width: 40
            height: 40
            source: isPlaying===true?"icons/pause.svg":"icons/play.svg"
            MouseArea {
                anchors.fill: parent
                onPressed:isPlaying===true? mediaPlayer.pause():mediaPlayer.play();
            }
        }

        Image {
            width: 40
            height: 40
            anchors.verticalCenter: parent
            source: isFullScreen===true ? "icons/windowed.svg":"icons/fullscreen.svg"
            MouseArea {
                anchors.fill: parent
                onPressed: {
                    isFullScreen = !isFullScreen
                }
            }
        }
    }
}
