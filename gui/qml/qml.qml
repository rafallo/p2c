import QtQuick 2.1
import QtQuick.Controls 1.1



Rectangle {
    width: 935
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
    ScrollView{
        anchors.bottom: mainWindow.bottom
        anchors.top: categories.bottom
        width: mainWindow.width
        GridView{
            id: movies
            clip:true
            cellWidth: 116; cellHeight: 116
            snapMode: GridView.SnapOneRow
            onContentYChanged:  {
//                console.log(contentY)
//                console.log(height)
            }

            onAtYEndChanged: {
//                console.log("1")
            }

            delegate: Item{
                width: 116
                height: 116
                Tile {
                    anchors.centerIn:parent
                    titleText: name
                    subtitleText: source
                    backgroundImage: poster
                    onTileClicked: {
                        movieClicked(index)
                    }
                }
            }

            model: moviesModel
        }}
    Player {}
}
