import QtQuick 2.0
Item {
    function show() {
        sidebarRec.x = parent.width - sidebarRec.width
    }
    function hide(){
        sidebarRec.x =  parent.width
    }

    signal exit()
    Rectangle {
        z: 23
        x: parent.parent.width
        height: parent.parent.height
        id:sidebarRec
        width: 220
        color: "black"
        Behavior on x{ PropertyAnimation {} }
        Rectangle {
            anchors {
                top : parent.top
            }
            width: parent.width
            height: 50
            color: "#e67e22"

            Text {
                text: "Type to search"
                color: 'white'
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                width: parent.width
                height: 30
                horizontalAlignment: TextInput.AlignHCenter
                visible: search.text.length == 0
                font { family: "Nokia Sans S60"; pixelSize: 22 }
            }

            TextInput {
                font { family: "Nokia Sans S60"; pixelSize: 22 }
                id: search
                color: "white"
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                width: parent.width
                height: 30
                horizontalAlignment: TextInput.AlignHCenter
                onTextChanged: {
                    searchQuery(text)
                }
            }
        }
        Rectangle {
            width: parent.width
            height: 50
            color: "#9b59b6"
            anchors.bottom: parent.bottom
            anchors.topMargin: 5
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    exit();
                }

            }
            Text {
                font { family: "Nokia Sans S60"; pixelSize: 22 }
                text: "Exit"
                color: 'white'
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                height: 30
            }

        }
    }

    MouseArea {
        x: parent.parent.width - 20
        width: 20
        height: parent.parent.height
        hoverEnabled: true
        onHoveredChanged: {
            width = sidebarRec.width + 20
            x = parent.parent.width - sidebarRec.width - 20
            parent.show()
        }
        onExited: {
            x = parent.parent.width - 20
            width = 20
            parent.hide()
        }
    }
}
