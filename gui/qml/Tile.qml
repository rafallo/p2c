import QtQuick 2.1

Item {
    width: 98
    height: 98
    property alias titleText: title.text
    property alias subtitleText: subtitle.text
    property alias background: back.color

    objectName: "tile"

    signal tileClicked()


    Rectangle {
        id: back
        anchors.fill: parent
        border.width: 0
        objectName: "backCase"
    }
    Text {
        id: title
        y: 5
        anchors.horizontalCenter: parent.horizontalCenter
        color: "white"
        wrapMode:Text.WordWrap
        width: 98
        height: 44
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignTop
        clip: true
    }
    Text {
        id: subtitle
        y: 50
        color: "#C9C9C9"
        wrapMode:Text.WordWrap
        width: 98
        height: 44
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        anchors.horizontalCenter: parent.horizontalCenter
        clip: true
    }
    MouseArea {
        id: mousearea
        anchors.fill: parent
        hoverEnabled: true

        onClicked: {
            rot.angle = 360

        }
        Component.onCompleted: {
            mousearea.clicked.connect(tileClicked)
        }
        onHoveredChanged: {
            rot.angle = -20

        }

        onExited: {
            rot.angle = 0
        }
    }
    transform: Rotation {
        id: rot
        origin.x: 49
        origin.y: 49
        axis.x: 0
        axis.y: 1
        axis.z: 0
        angle: 0

        Behavior on angle {
            PropertyAnimation {
                duration: 300
            }
        }
    }
}
