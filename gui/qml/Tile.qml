import QtQuick 2.1


Item {
    width: stretched == false?112:228
    height: 112

    property alias titleText: title.text
    property alias subtitleText: subtitle.text
    property alias descriptionText: description.text
    property alias backgroundImage: cover.source
    property bool resizableForMoreInfo: false;

    property bool stretched: false;
    property int circles: 0

    objectName: "tile"

    signal tileClicked()

    function animateAndClick() {
        circles += 1
        rot.angle = circles * 360
        tileClicked();
    }

    Behavior on width {
        PropertyAnimation {
        }
    }

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
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onClicked: {
            if(resizableForMoreInfo == false){
                animateAndClick()
            } else {
                stretched = !stretched;
            }
        }
        onHoveredChanged: {
            rot.angle = (circles * 360) + 20
        }
        onExited: {
            rot.angle = (circles * 360)
        }
    }
    Image {
        id: cover
        anchors.left: parent.left
        anchors.top: parent.top
        width: 112
        height: 112
    }
    Rectangle {
        id: back
        anchors.left: parent.left
        anchors.top: parent.top
        width: 112
        height: 112
        color: backgroundImage != ''? Qt.rgba(0,0,0,0.7): randomBackground(titleText + subtitleText)
        opacity: backgroundImage != '' ? 0.7:1
    }

    Rectangle {
        anchors.left: back.right
        anchors.top: parent.top
        width: stretched === true?116:0
        clip: true
        height: 112
        Behavior on width {
            PropertyAnimation {
            }
        }
        color: randomBackground(titleText + subtitleText)

        Text {
            id: description
            anchors {
                top: parent.top
                topMargin: 5
            }
            color: "white"
            wrapMode:Text.WordWrap
            width: 112
            height: 80
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignLeft
            clip: true
            font.pixelSize: 12
        }

        Rectangle {
            anchors {
                bottom: parent.bottom
                right: parent.right
                rightMargin: 10
                bottomMargin: 5
            }
            width: 80; height: 23
            color: "white"
            radius: 10
            Text{
                text: "Play!"
                anchors.horizontalCenter: parent.horizontalCenter
                font.pixelSize: 16
            }

            MouseArea {
                anchors.fill: parent
                onClicked: animateAndClick()
            }
        }
    }


    Text {
        id: title
        y: 5
        anchors.horizontalCenter: back.horizontalCenter
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
        anchors.horizontalCenter: back.horizontalCenter
        clip: true
        font.pixelSize: 10
    }

    transform: Rotation {
        id: rot
        origin.x: stretched == true ?114:56
        origin.y: 56
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
