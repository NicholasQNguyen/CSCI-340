To Run:
python3 rayTracer.py -f [FILE_NAME] -sh [ShowType] -s [Sample per Pixel] -csx [ChunkStartX] -csy [ChunkStartY]
or 
make run

Flags:
-f -> File Name: Name of file if you save it.

-sh -> Show Type: Type of show to do (PerColumn, PerPixel, NoShow, etc.)
NOTE: if -sh is set to NoShow, -f must also be set or an exception will raise

-s -> Sample: Sample per pixel for the anti aliasing.

-csx -> ChunkStartX: X chunk to start on when using quilt renderer

-csy -> ChunkStartY: Y chunk to start on when using quilt renderer
