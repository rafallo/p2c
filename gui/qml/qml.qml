import QtQuick 2.1
import QtQuick.Controls 1.1



Rectangle {
    width: 945
    height: 600
    id: mainWindow

    property int latestIndex: 0;
    property bool isMovieScene: false;
    anchors.margins:5

    signal categoryClicked(int index)
    signal movieClicked(int index)
    signal searchQuery(string query)

    onCategoryClicked: {
        search.text = ''
        search.focus = false
    }

    // categories
    Item {
        id: menuBar
        width: 132
        height: mainWindow.height - 8
        Text {
            text: "Search"
            color: 'gray'
            anchors.top: parent.top
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.topMargin: 5
            width: 120
            height: 30
            horizontalAlignment: TextInput.AlignHCenter
            visible: search.text.length == 0
            font { family: "Nokia Sans S60"; pixelSize: 16 }
        }

        TextInput {
            font { family: "Nokia Sans S60"; pixelSize: 16 }
            id: search
            anchors.top: parent.top
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.topMargin: 5
            width: 120
            height: 30
            horizontalAlignment: TextInput.AlignHCenter
            onTextChanged: {
                searchQuery(text)
            }
        }
        ScrollView {
            anchors.margins: 4
            anchors.top: search.bottom
            height: mainWindow.height - 8-40
            width: 132
            x: 4
            y: 4

            Column {
                spacing: 4
                Repeater {
                    id: rep
                    model: categoriesModel
                    objectName: "categoriesContainer"
                    Tile {
                        titleText: name
                        subtitleText: source
                        backgroundImage: poster
                        resizableForMoreInfo: false
                        onTileClicked: {
                            categoryClicked(index)
                        }
                    }
                }
            }
        }
    }

    // movies

    ScrollView {
        id: movies
        anchors {
            bottom: mainWindow.bottom
            right: mainWindow.right
            top: mainWindow.top
            left: menuBar.right
            topMargin: 4
            leftMargin: 4
        }

        Flow {
            width: mainWindow.width - 160
            spacing: 4
            Repeater {
                model: moviesModel
                Tile {
                    titleText: name
                    subtitleText: source
                    backgroundImage: poster
                    descriptionText: description
                    resizableForMoreInfo: true
                    onTileClicked: {
                        movieClicked(index)
                    }
                }
            }
        }
    }


    Player {
        width: mainWindow.width
        height: mainWindow.height
    }
}
