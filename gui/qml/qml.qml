import QtQuick 2.1
import QtQuick.Controls 1.1



Rectangle {
    width: 1024
    height: 600
    id: mainWindow

    property int latestIndex: 0;
    property bool isMovieScene: false;
    anchors.margins:5

    signal categoryClicked(int index)
    signal movieClicked(int index)


    // categories
    ScrollView {
        id: categories
        width: mainWindow.width - 8
        anchors.margins: 4
        height: 132
        x: 4
        y: 4
        Row {
            spacing: 4
            Repeater {
                id: rep
                model: categoriesModel
                objectName: "categoriesContainer"
                Tile {
                    titleText: name
                    subtitleText: source
                    backgroundImage: poster
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
        width: mainWindow.width - 8
        anchors.margins: 4
        x: 4
        anchors.bottom: mainWindow.bottom
        anchors.top: categories.bottom
        Flow {
            spacing: 4
            width: mainWindow.width
            Repeater {
                model: moviesModel
                Tile {
                    titleText: name
                    subtitleText: source
                    backgroundImage: poster
                    onTileClicked: {
                        movieClicked(index)
                    }
                }
            }
        }
    }
    Player {}
}
