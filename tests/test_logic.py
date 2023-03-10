import pytest
import sys

sys.path.append(".")


from proplogic.logic_parser import LogicParser
from proplogic.truth_value_assignment import TruthValueAssignmentVisitor
import logging


logging.basicConfig(filename='logic_parser.log', level=logging.DEBUG)



class TestLogicParser(object):
    
    def test_simple(self):
        
        parser = LogicParser("a")
        assert str(parser.parse()) == "a"
        
    def test_simple_and(self):
        
        parser = LogicParser("a & b")
        assert str(parser.parse()) == "a & b"
        
    def test_simple_or(self):
        
        parser = LogicParser("a | b")
        assert str(parser.parse()) == "a | b"
        
    def test_simple_neg(self):
        
        parser = LogicParser("~a")
        assert str(parser.parse()) == "~a"
    
    def test_simple_paren(self):
            
        parser = LogicParser("(a)")
        assert str(parser.parse()) == "a"
    
    def test_simple_paren2(self):
        
        parser = LogicParser("((a))")
        assert str(parser.parse()) == "a"
        
    def test_simple_paren3(self):
            
        parser = LogicParser("()")
        
        # assert error
        with pytest.raises(Exception):
            parser.parse() 
            
    def test_simple_paren4(self):
                
        parser = LogicParser("(a")
        
        # assert error
        with pytest.raises(Exception):
            parser.parse()
        
    def test_complex1(self):
        
        parser = LogicParser("a & b | c & d")
        assert str(parser.parse()) == "(a & b) | (c & d)"
    
    def test_complex2(self):
            
            parser = LogicParser("a | b & c | d")
            assert str(parser.parse()) == "(a | (b & c)) | d"
    
    def test_complex3(self):
    
        parser = LogicParser("a & b | ( c & d | e )")
        assert str(parser.parse()) == "(a & b) | ((c & d) | e)"
        
    
    def test_complex4(self):
    
        parser = LogicParser("a | b & ~c & d | d & ~ ~  ~ e")
        print (f"parser.parse() is {parser.ast}")
        assert str(parser.ast) == "(a | ((b & (~c)) & d)) | (d & (~(~(~e))))"
    
    def test_visualize(self):
        
        parser = LogicParser("a & b | c & d")
        tree = parser.parse()
        tree.visualizeAST()
        
    
class TestTruthValueAssignment(object):
    
    def test_simple(self):
        
        parser = LogicParser("a")
        ast = parser.parse()
        visitor = TruthValueAssignmentVisitor({"a":True})
        assert ast.accept(visitor) == True
        
        visitor = TruthValueAssignmentVisitor({"a":False})
        assert ast.accept(visitor) == False
        
    
    def test_simple_and(self):
        
        parser = LogicParser("a & b")
        ast = parser.parse()
        visitor = TruthValueAssignmentVisitor({"a":True, "b":True})
        assert ast.accept(visitor) == True
        
        visitor = TruthValueAssignmentVisitor({"a":True, "b":False})
        assert ast.accept(visitor) == False
        
        visitor = TruthValueAssignmentVisitor({"a":False, "b":True})
        assert ast.accept(visitor) == False
        
        visitor = TruthValueAssignmentVisitor({"a":False, "b":False})
        assert ast.accept(visitor) == False
    
    def test_simple_or(self):
        
        parser = LogicParser("a | b")
        ast = parser.parse()
        visitor = TruthValueAssignmentVisitor({"a":True, "b":True})
        assert ast.accept(visitor) == True
        
        visitor = TruthValueAssignmentVisitor({"a":True, "b":False})
        assert ast.accept(visitor) == True
        
        visitor = TruthValueAssignmentVisitor({"a":False, "b":True})
        assert ast.accept(visitor) == True
        
        visitor = TruthValueAssignmentVisitor({"a":False, "b":False})
        assert ast.accept(visitor) == False
    
    def test_simple_neg(self):
        
        parser = LogicParser("~a")
        ast = parser.parse()
        visitor = TruthValueAssignmentVisitor({"a":True})
        assert ast.accept(visitor) == False
        
        visitor = TruthValueAssignmentVisitor({"a":False})
        assert ast.accept(visitor) == True
    
    def test_simple_paren(self):
        
        parser = LogicParser("(a)")
        ast = parser.parse()
        visitor = TruthValueAssignmentVisitor({"a":True})
        assert ast.accept(visitor) == True
        
        visitor = TruthValueAssignmentVisitor({"a":False})
        assert ast.accept(visitor) == False
    
    
        
    
    def test_complex1(self):
        
        parser = LogicParser("a & b | c & d")
        ast = parser.parse()
        visitor = TruthValueAssignmentVisitor({"a":True, "b":True, "c":True, "d":True})
        assert ast.accept(visitor) == True
        
        visitor = TruthValueAssignmentVisitor({"a":True, "b":True, "c":True, "d":False})
        assert ast.accept(visitor) == True
        
        visitor = TruthValueAssignmentVisitor({"a":True, "b":True, "c":False, "d":True})
        assert ast.accept(visitor) == True
        
        visitor = TruthValueAssignmentVisitor({"a":True, "b":True, "c":False, "d":False})
        assert ast.accept(visitor) == True
        
        visitor = TruthValueAssignmentVisitor({"a":True, "b":False, "c":True, "d":True})
        assert ast.accept(visitor) == True
        
        visitor = TruthValueAssignmentVisitor({"a":True, "b":False, "c":True, "d":False})
        assert ast.accept(visitor) == False
        
        visitor = TruthValueAssignmentVisitor({"a":True, "b":False, "c":False, "d":True})
        assert ast.accept(visitor) == False
        
        visitor = TruthValueAssignmentVisitor({"a":True, "b":False, "c":False, "d":False})
        assert ast.accept(visitor) == False
        
        visitor = TruthValueAssignmentVisitor({"a":False, "b":True, "c":True, "d":True})
        assert ast.accept(visitor) == True
        
        visitor = TruthValueAssignmentVisitor({"a":False, "b":True, "c":True, "d":False})
        assert ast.accept(visitor) == False
        
        visitor = TruthValueAssignmentVisitor({"a":False, "b":True, "c":False, "d":True})
        assert ast.accept(visitor) == False
        
        visitor = TruthValueAssignmentVisitor({"a":False, "b":True, "c":False, "d":False})
        assert ast.accept(visitor) == False
        
        visitor = TruthValueAssignmentVisitor({"a":False, "b":False, "c":True, "d":True})
        assert ast.accept(visitor) == True
        

    
