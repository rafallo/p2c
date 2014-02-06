import QtQuick 2.0

Rectangle {
    width: playerArea.width
    height: 80
    color: "black"
    SeekControl {
        anchors {
            left: parent.left
            right: parent.right
            leftMargin: 100
            rightMargin: 140
            bottom: parent.bottom
        }
        duration: mediaPlayer ? mediaPlayer.duration : 0
        playPosition: mediaPlayer ? mediaPlayer.position : 0
        onSeekPositionChanged: { mediaPlayer.seek(seekPosition); }
    }

    Row {
        Rectangle {
            width: 80
            height: 40
            anchors.verticalCenter: parent
            Text{
                text: isPlaying===true?"PAUSE":"PLAY"
                anchors.centerIn: parent
            }
            MouseArea {
                anchors.fill: parent
                onPressed:isPlaying===true? mediaPlayer.pause():mediaPlayer.play();
            }
        }

        Rectangle {
            width: 80
            height: 40
            anchors.verticalCenter: parent
            Text{
                text: isFullScreen === true ? "SMALL SCREEN" : "FULLSCREEN"
                anchors.centerIn: parent
            }
            MouseArea {
                anchors.fill: parent
                onPressed: {
                    isFullScreen = !isFullScreen
                }
            }
        }
    }
}
