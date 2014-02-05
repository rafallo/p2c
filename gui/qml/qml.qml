import QtQuick 2.1
import QtQuick.Controls 1.1
import QtMultimedia 5.0


//![0]
Rectangle {
    width: 800
    height: 600
    id: mainWindow

    anchors.margins:5
    property int latestIndex: 0;

    signal categoryClicked(int index)

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

    // categories
    ScrollView {
        id: categories
        width: mainWindow.width
        height: 120
        anchors.top: parent.top
        anchors.left: parent.left

        Row {
            Repeater {
                id: rep
                model: categoriesModel
                objectName: "categoriesContainer"

                Tile {
                    titleText: name
                    subtitleText: source
                    background: randomBackground(name + source)
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
        width: mainWindow.width
        //anchors.bottom: mainWindow.bottom
        anchors.top: categories.bottom

        Flow {
            width: mainWindow.width
            anchors.bottom: mainWindow.bottom
            anchors.top: categories.bottom
            Repeater {
                model: moviesModel

                Tile {
                    titleText: name
                    subtitleText: source
                    background: randomBackground(name + source)

                }
            }


        }}
    MediaPlayer {
            id: mediaPlayer
            source: movieSource
        }
    VideoOutput {
        id: mediaOutput
//        anchors.top: movies.bottom
           anchors.top: movies.top
           source: mediaPlayer
       }
    MouseArea {
           id: playArea
//           anchors.top: movies.top
           anchors.fill: mediaOutput
           onPressed: mediaPlayer.play();
       }
}


//    ScrollView{
//        width: mainWindow.width
//        height: categories.contentHeight
//        id:categoriesScroll
//        objectName: "categoriesContainer"

//        Row {
//            objectName: "categories"
//            id: categories
//            anchors.top: mainWindow.top
//            anchors.left: mainWindow.left
//            spacing: 10
//            anchors.margins: 20
//            Repeater {
//                objectName: "repeater"
////                model: Tile
////                Tile {
////                    labelText: qsTr("Kategoria " + (index + 1))
////                }
//            }
//        }
//    }


// movies
//    ScrollView{
//        id:moviesScroll
//        width: mainWindow.width
//        height: mainWindow.height  - categoriesScroll.height - 20
//        y: 200
//        //anchors.top: 200//categoriesScroll.bottom
//        Flow {
//            width: moviesScroll.width - 20
//            id: movies
//            spacing: 10


//            anchors.topMargin: 20
//            anchors.margins: 20
//            Repeater {
//                model: 10
//                Tile {
//                    labelText: qsTr("Film " + (index + 1))
//                }
//            }
//        }
//    }
//![0]
