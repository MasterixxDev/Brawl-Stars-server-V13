from Utils.BitStream import BitStream
from Utils.Helpers import Helpers
from Utils.Writer import Writer 

class GameObjects:

    def encode(stream, self):
        stream.writePositiveInt(1000000 + 0, 21)
        stream.writePositiveVInt(0, 4)
        stream.writePositiveInt(0, 1)
        stream.writeInt(-1, 4)  # понос

        stream.writePositiveInt(1, 1)
        stream.writePositiveInt(1, 1)
        stream.writePositiveInt(1, 1)
        stream.writePositiveInt(0, 1)

        stream.writePositiveInt(0, 5)
        stream.writePositiveInt(0, 6)
        stream.writePositiveInt(0, 5)
        stream.writePositiveInt(0, 6)

        stream.writeBoolean(False)
        for i in range(6):
            stream.writeBoolean(False)
            stream.writeBoolean(False)
            if i == 1:
                stream.writePositiveInt(0, 12)
                stream.writeBoolean(False)
                stream.writeBoolean(False)
        stream.writePositiveInt(1, 1)
        for i in range(6):
            stream.writePositiveInt(0, 1)
            stream.writePositiveInt(0, 1)

        # GameObjects start
        stream.writePositiveInt(1, 7)  # count

        # objects config start
        stream.writePositiveInt(16, 5)
        stream.writePositiveInt(0, 8)  # id
        # objects config end

        # IDs start
        stream.writePositiveInt(0, 14)
        # IDs end

        # player start
        stream.writePositiveVInt(self.player.battleX, 4)  # x spawn
        stream.writePositiveVInt(self.player.battleY, 4)  # y spawn
        stream.writePositiveVInt(0, 3)  # i
        stream.writePositiveVInt(0, 4)  # z

        stream.writePositiveInt(10, 4)
        stream.writePositiveInt(0, 1)
        stream.writePositiveInt(0, 3)
        stream.writePositiveInt(0, 1)
        stream.writeInt(63, 6)
        stream.writePositiveInt(0, 1)
        stream.writePositiveInt(0, 1)
        stream.writePositiveInt(0, 1)
        stream.writePositiveInt(0, 1)
        stream.writePositiveInt(1, 1)
        stream.writePositiveInt(1, 1)
        stream.writePositiveInt(0, 1)
        stream.writePositiveInt(0, 1)
        stream.writePositiveInt(0, 2)
        stream.writePositiveInt(3599, 13)
        stream.writePositiveInt(3600, 13)
        stream.writePVIntMax255OZ(0)
        stream.writePVIntMax255OZ(0)
        #player end
        
        #остальное
        stream.writePositiveInt(0, 1)
        stream.writePositiveInt(0, 1)
        stream.writePositiveInt(0, 1)
        stream.writePositiveInt(0, 1)
        stream.writePositiveInt(0, 1)
        stream.writePositiveInt(0, 1)
        stream.writePositiveInt(0, 4)
        stream.writePositiveInt(0, 2)
        stream.writePositiveInt(0, 1)
        stream.writePositiveInt(0, 9)
        stream.writePositiveInt(0, 1)
        stream.writePositiveInt(0, 1)

        stream.writePositiveInt(0, 5)

        stream.writePVIntMax255OZ(0)
        stream.writePositiveInt(0, 1)
        stream.writePVIntMax255OZ(0)
        stream.writePositiveInt(3000, 12)
        stream.writePVIntMax255OZ(0)
        stream.writePositiveInt(0, 1)
        stream.writePVIntMax255OZ(0)