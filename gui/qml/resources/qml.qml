import QtQuick 2.1
import QtQuick.Controls 1.1


Rectangle {
    width: 945
    height: 600
    id: mainWindow

    property int latestIndex: 0;
    property bool isMovieScene: false;
    property int movieDuration: 0;
    property string debugText: "";
    anchors.margins:5

    signal categoryClicked(int index)
    signal movieClicked(int index)
    signal searchQuery(string query)

    // actions
    signal exitAction()

    onCategoryClicked: {
        search.text = ''
        search.focus = false
    }

    // categories
    ScrollView {
        id: menuBar
        anchors.margins: 4
        anchors.top: search.bottom
        height: mainWindow.height - 8
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
    Rectangle {
        visible: loadingMask
        anchors {
            fill: movies
        }
        color: Qt.rgba(255,255,255, 0.7)
        AnimatedImage {
            visible: loadingMask
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            width: 32
            height: 32
            source: "qrc:icons/loader.gif"
        }
    }

    Player {
        width: mainWindow.width
        height: mainWindow.height
    }

    Sidebar{
        id: sidebar
        onExit: exitAction()
    }
}
