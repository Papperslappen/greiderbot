import unittest
import command as cmd

@cmd.command("test")
def testCommand(args):
    return args

@cmd.command("test2",timeout=1000)
def timeoutTestCommand(args):
    return args

def testCommand2(args):
    return args

class CommandTestCases(unittest.TestCase):
    def testSimpleCommand(self):
        result = testCommand("test")
        self.assertTrue(result.type == cmd.ResultType.VALUE)
        self.assertTrue(result.value == "test")

    def testTimeout(self):
        result1 = timeoutTestCommand("test")
        result2 = timeoutTestCommand("test")
        self.assertTrue(result1.type == cmd.ResultType.VALUE)
        self.assertTrue(result2.type == cmd.ResultType.TIMEOUT)

    def testGetCommand(self):
        self.assertTrue(cmd.isCommand("test"))
        self.assertFalse(cmd.isCommand("Idonotexist"))
        command = cmd.getCommand("test")
        self.assertTrue(command.do("asdf").value == "asdf")
        command = cmd.getCommand("Idonotexist") #test for nonexistent command
        self.assertTrue(command.do("asdf").value == "")
        self.assertTrue(command.do("asdf").type == cmd.ResultType.EMPTY)


    def testRegisterCommand(self):
        cmd.registerCommand("test3",testCommand2,timeout=0,attributes = [])
        print("Testing result: {}".format(cmd.getCommand("test3").do("flonk").value))
        self.assertTrue(cmd.getCommand("test3").do("flonk").value == "flonk")


if __name__ == '__main__':
    unittest.main()
