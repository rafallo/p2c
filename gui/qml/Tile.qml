import QtQuick 2.1


Item {
    width: 112
    height: 112

    property alias titleText: title.text
    property alias subtitleText: subtitle.text
    property alias backgroundImage: cover.source

    objectName: "tile"

    signal tileClicked()

    function randomBackground (name)
    {
        var qml= new Array ("#1abc9c", "#2ecc71", "#3498db",
                            "#9b59b6","#34495e","#f1c40f","#e67e22","#e74c3c","#95a5a6"
                            )
        var currentIndex = name.length % qml.length;
        var bg = qml[currentIndex]
        latestIndex = currentIndex
        return bg
    }

    Image {
        id: cover
        anchors.fill: parent
    }
    Rectangle {
        id: back
        anchors.fill: parent
        color: backgroundImage != ''? Qt.rgba(0,0,0,0.7): randomBackground(titleText + subtitleText)
        opacity: backgroundImage != '' ? 0.7:1
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
        font.pixelSize: 12
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
        font.pixelSize: 10
    }
    MouseArea {
        id: mousearea
        anchors.fill: parent
        hoverEnabled: true
        property int circles: 0
        onClicked: {
            circles += 1
            rot.angle = circles * 360
        }
        Component.onCompleted: {
            mousearea.clicked.connect(tileClicked)
        }
        onHoveredChanged: {
            rot.angle = (circles * 360) + 20
        }
        onExited: {
            rot.angle = (circles * 360)
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
