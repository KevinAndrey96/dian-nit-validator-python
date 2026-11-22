"""
Unit tests for Python Algorithmic Exercises
Testing NIT DIAN validation, robot state machine, and student grading aggregation.
"""

import unittest
from verification import verificar_nit
from robot import girar, movimiento_robot
from student import mejor_de_cada_curso


class TestExercises(unittest.TestCase):

    def test_verificar_nit_valid(self):
        # 860007386 - 1 (Bancolombia S.A.)
        self.assertTrue(verificar_nit(860007386, 1))

    def test_verificar_nit_invalid(self):
        # Incorrect check digit
        self.assertFalse(verificar_nit(860007386, 9))

    def test_robot_rotations(self):
        self.assertEqual(girar('N', 'R'), 'E')
        self.assertEqual(girar('N', 'L'), 'W')
        self.assertEqual(girar('N', 'H'), 'S')
        self.assertEqual(girar('N', '.'), 'N')

    def test_robot_sequence(self):
        # Facing North: Right -> East; Half-turn -> West; Keep -> West
        self.assertEqual(movimiento_robot('N', 'R', 'H', '.'), 'W')

    def test_student_grading(self):
        s1 = {"nombre": "A", "matematicas": 5.0, "español": 1.0, "ciencias": 2.0, "literatura": 2.0, "arte": 2.0}
        s2 = {"nombre": "B", "matematicas": 1.0, "español": 5.0, "ciencias": 2.0, "literatura": 2.0, "arte": 2.0}
        s3 = {"nombre": "C", "matematicas": 1.0, "español": 1.0, "ciencias": 5.0, "literatura": 2.0, "arte": 2.0}
        s4 = {"nombre": "D", "matematicas": 1.0, "español": 1.0, "ciencias": 1.0, "literatura": 5.0, "arte": 2.0}
        s5 = {"nombre": "E", "matematicas": 1.0, "español": 1.0, "ciencias": 1.0, "literatura": 1.0, "arte": 5.0}

        best = mejor_de_cada_curso(s1, s2, s3, s4, s5)
        self.assertEqual(best["matematicas"], "A")
        self.assertEqual(best["español"], "B")
        self.assertEqual(best["ciencias"], "C")
        self.assertEqual(best["literatura"], "D")
        self.assertEqual(best["arte"], "E")


if __name__ == '__main__':
    unittest.main()
