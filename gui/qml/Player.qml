import QtQuick 2.0
import QtMultimedia 5.0

Rectangle {
    property bool isFullScreen: false
    property bool isPlaying: false

    visible: isMovieScene
    id:playerArea
    color: isFullScreen === true ? Qt.rgba(0,0,0,1) : Qt.rgba(0,0,0,0.8)
    Behavior on color{ PropertyAnimation {} }
    anchors.fill: mainWindow.fill
    anchors.top: mainWindow.top
    width: 800
    height: 600

    Text {
        text: movieStatus
        anchors.centerIn: parent
        color: "white"
        font.pixelSize: 30
    }
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onClicked: {
            mediaPlayer.pause()
            isFullScreen = false
            isMovieScene = false
        }
    }

    MediaPlayer {
        property alias isPlaying: playerArea.isPlaying
        id: mediaPlayer
        source: movieSource
        onPaused: {
            isPlaying = false
            playerBar.show()
        }
        onStopped: {
            isPlaying = false
            playerBar.show()
        }
        onPlaying: {
            isPlaying = true
            playerBar.hide()
        }
    }
    VideoOutput {
        property alias isFullScreen: playerArea.isFullScreen
        visible: isPlaying
        opacity: 1
        id: videoOutput
        anchors.centerIn: playerArea
        source: mediaPlayer
        width: isFullScreen === true ? playerArea.width : playerArea.width * 0.8
        height: isFullScreen === true ? playerArea.height : playerArea.height * 0.8
        Behavior on width { PropertyAnimation {} }
        Behavior on height{ PropertyAnimation {} }
        MouseArea {
            property alias isPlaying: playerArea.isPlaying
            anchors.fill: parent
            onPressed: {
                isPlaying===true? mediaPlayer.pause():mediaPlayer.play();
            }
        }
    }
    // TODO: move belowed MouseArea to playerbar component (like in Sidebar component)
    MouseArea {
        anchors.bottom: parent.bottom
        width: parent.width
        height: playerBar.height + 20
        hoverEnabled: true
        onHoveredChanged: {
            playerBar.show()
        }
        onExited: {
            playerBar.hide()
        }
    }
    Playerbar {
        Behavior on y{ PropertyAnimation {} }
        id: playerBar
        y: parent.height - playerBar.height
        property alias isFullScreen: playerArea.isFullScreen
        property alias isPlaying: playerArea.isPlaying
        property alias mediaPlayer: mediaPlayer
        function show() {
            y = parent.height - playerBar.height

        }
        function hide(){
            y =  parent.height
        }

        onChangeVolume:{
            mediaPlayer.volume = level
        }
    }

}
