import unittest
import errors
from decl import decl
from func import func
from call import call
from cond import cond
from stop import stop
from store import store
from cps import receive
from environment import environment
from interpreter import stop_catch_interpretter
from prelude import ops, ops_mapping
from parse import parse, parseList
from alphaequal import alpha_equal
from declSequence import declSequence


class Tests(unittest.TestCase):
    def test_call(self):
        t_call = call(func([], 1), [])
        self.assertEqual(t_call.fun, func([], 1))
        self.assertEqual(t_call.params, [])
        t_call = call(func(["x"], 1), [1])
        self.assertEqual(t_call.fun, func(["x"], 1))
        self.assertEqual(t_call.params, [1])

    def test_cond(self):
        t_cond = cond(func([], 1), 1, 0)
        self.assertEqual(t_cond.condition, func([], 1))
        self.assertEqual(t_cond.true_expression, 1)
        self.assertEqual(t_cond.false_expression, 0)

    def test_decl(self):
        t_decl = decl("x", 1)
        self.assertEqual(t_decl.var, "x")
        self.assertEqual(t_decl.rhs, 1)
        t_decl = decl("x", func([], 1))
        self.assertEqual(t_decl.var, "x")
        self.assertEqual(t_decl.rhs, func([], 1))

    def test_declSequence(self):
        t_declSeq = declSequence([decl("x", 1), "x"])
        self.assertEqual(t_declSeq.sequence, [decl("x", 1)])
        self.assertEqual(t_declSeq.expr, "x")
        t_declSeq = declSequence([decl("x", 1), decl("x", func([], 1)), 1])
        self.assertEqual(t_declSeq.sequence, [decl("x", 1), decl("x", func([], 1))])
        self.assertEqual(t_declSeq.expr, 1)

    def test_func(self):
        t_func = func([], 1)
        self.assertEqual(t_func.args, [])
        self.assertEqual(t_func.body, 1)

    def test_parse(self):
        t_json = 1
        self.assertEqual(parse(t_json), 1)
        t_json = "a"
        self.assertEqual(parse(t_json), "a")
        t_json = ["a"]
        self.assertEqual(parse(t_json), ["a"])

    def test_parse_list(self):
        t_json = ["fun*", [], 1]
        self.assertEqual(parseList(t_json), func([], 1))
        t_json = ["call", "+", 1, 2]
        self.assertEqual(parseList(t_json), call("+", [1, 2]))
        t_json = ["let", "x", "=", ["fun*", [], 1]]
        self.assertEqual(parseList(t_json), decl("x", func([], 1)))
        t_json = ["a", "b", "c"]
        self.assertEqual(parseList(t_json), ["a", "b", "c"])

    def test_alpha_equals(self):
        self.assertTrue(alpha_equal("a", "b"))
        self.assertTrue(not alpha_equal(1, "b"))
        self.assertTrue(alpha_equal(func("a", "a"), func("b", "b")))
        self.assertTrue(alpha_equal(declSequence([decl("x", func("a", "a")), "x"]),
                                    declSequence([decl("asdf", func("gfd", "gfd")), "asdf"])))

    def test_cps(self):
        # Using the alpha_equals() for equality

        t_json = 1
        parsed_json = parse(t_json)
        cps = receive(parsed_json)
        test = func(["k1"], call("k1", [1]))
        self.assertTrue(alpha_equal(cps, test))

        t_json = "a"
        parsed_json = parse(t_json)
        cps = receive(parsed_json)
        test = func(["k2"], call("k2", ["a"]))
        self.assertTrue(alpha_equal(cps, test))

        t_json = "+"
        parsed_json = parse(t_json)
        cps = receive(parsed_json)
        test = func(["k3"], call("k3", ops_mapping["+"]))
        self.assertTrue(alpha_equal(cps, test))

        t_json = ["call", ["fun*", ["x", "y"], "y"], 1, 2]
        parsed_json = parse(t_json)
        cps = receive(parsed_json)
        test = func("k5", call(func("k6", call("k6", 2)),
                               func("of-1", call(func("k7", call("k7", 1)),
                                                 func("of-0",
                                                      call(func(["k8"],
                                                                call("k8",
                                                                     func(["k", "x", "y"], call("k", "y")))),
                                                           func("of-f",
                                                                call("of-f", ["k5", "of-0", "of-1"]))))))))
        self.assertTrue(alpha_equal(cps, test))

        t_json = ["if-0", 0, 1, 2]
        parsed_json = parse(t_json)
        cps = receive(parsed_json)
        test = func(["k9"], call(func(["k10"], call("k10", [0])), func(["of-tst"], cond("of-tst",
                                                                                        call("k9", [1]),
                                                                                        call("k9", [2])))))
        self.assertTrue(alpha_equal(cps, test))

        t_json = [["let", "a", "=", 5], ["let", "b", "=", 6], "b"]
        parsed_json = parse(t_json)
        cps = receive(parsed_json)
        test = declSequence([decl("a", 5), decl("b", 6), func(["k11"], call("k11", ["b"]))])
        self.assertTrue(alpha_equal(cps, test))

        t_json = ["fun*", ["x"], "x"]
        parsed_json = parse(t_json)
        cps = receive(parsed_json)
        test = func(["k12"], call("k12", func(["k", "x"], call("k", ["x"]))))
        self.assertTrue(alpha_equal(cps, test))

        # Unit tests against names we would generate
        t_json = ["fun*", ["kb"], "kb"]
        parsed_json = parse(t_json)
        cps = receive(parsed_json)
        test = func(["k12"], call("k12", func(["k", "kb"], call("k", ["kb"]))))
        self.assertTrue(alpha_equal(cps, test))

        t_json = ["call", "+", 1, 2]
        parsed_json = parse(t_json)
        cps = receive(parsed_json)
        test = func("k13", call(func("k14", call("k14", 2)),
                                func("of-1",
                                     call(func("k15", call("k15", 1)),
                                          func("of-0", call(func("k", call("k", ops_mapping["+"])),
                                                            func("k", call("k", ["k13", "of-0", "of-1"]))))))))
        self.assertTrue(alpha_equal(cps, test))

        t_json = ["grab", "x", ["call", "x", 10]]
        parsed_json = parse(t_json)
        cps = receive(parsed_json)
        test = func(["k"], declSequence([decl("x", func(["x", "f"], call("k", "f"))),
                                         call(func("kc", call("kc", 10)),
                                              func("fa",
                                                   call(func("kd", call("kd", "x")),
                                                        func("fb", call("fb", ["kb", "fa"])))))]))
        self.assertTrue(alpha_equal(cps, test))

        t_json = ["stop", 10]
        parsed_json = parse(t_json)
        cps = receive(parsed_json)
        test = func("k", stop(func("kc", call("kc", 10))))
        self.assertTrue(alpha_equal(cps, test))

        t_json = ["call", "+", 1, ["stop", 10]]
        parsed_json = parse(t_json)
        cps = receive(parsed_json)
        test = func("k13", call(func("k", stop(func("kc", call("kc", 10)))),
                                func("of-1",
                                     call(func("k15", call("k15", 1)),
                                          func("of-0", call(func("k", call("k", ops_mapping["+"])),
                                                            func("k", call("k", ["k13", "of-0", "of-1"]))))))))
        self.assertTrue(alpha_equal(cps, test))

        t_json = declSequence([decl("x", 15), "x"])
        cps = receive(t_json)
        test = declSequence([decl("x", 15), func("ke", call("ke","x"))])
        self.assertTrue(alpha_equal(cps, test))

    def test_interpret(self):
        t_json = 1
        parsed_json = parse(t_json)
        toy = receive(parsed_json)
        env, store_ = interpret_init()
        result, new_store = stop_catch_interpretter(call(toy, func(["x"], "x")), env, store_)
        self.assertEqual(result, 1)

        t_json = ["fun*", [], 1]
        parsed_json = parse(t_json)
        toy = receive(parsed_json)
        env, store_ = interpret_init()
        result, new_store = stop_catch_interpretter(call(toy, func(["x"], "x")), env, store_)
        self.assertEqual(str(result), "\"closure\"")

        t_json = "!"
        parsed_json = parse(t_json)
        toy = receive(parsed_json)
        env, store_ = interpret_init()
        result, new_store = stop_catch_interpretter(call(toy, func(["x"], "x")), env, store_)
        self.assertEqual(str(result), "\"closure\"")

        t_json = ["call", "@", 1]
        parsed_json = parse(t_json)
        toy = receive(parsed_json)
        env, store_ = interpret_init()
        result, new_store = stop_catch_interpretter(call(toy, func(["x"], "x")), env, store_)
        self.assertEqual(str(result), "\"cell\"")

        t_json = "a"
        parsed_json = parse(t_json)
        toy = receive(parsed_json)
        env, store_ = interpret_init()
        self.assertRaises(errors.UndeclaredException,
                          stop_catch_interpretter, call(toy, func(["x"], "x")), env, store_)

        t_json = ["call", "^", 1, -1]
        parsed_json = parse(t_json)
        toy = receive(parsed_json)
        env, store_ = interpret_init()
        self.assertRaises(errors.exponentiationError,
                          stop_catch_interpretter, call(toy, func(["x"], "x")), env, store_)

        t_json = ["call", "^", 1]
        parsed_json = parse(t_json)
        toy = receive(parsed_json)
        env, store_ = interpret_init()
        self.assertRaises(errors.ArgumentParameterMismatch,
                          stop_catch_interpretter, call(toy, func(["x"], "x")), env, store_)

        t_json = ["call", 1]
        parsed_json = parse(t_json)
        toy = receive(parsed_json)
        env, store_ = interpret_init()
        self.assertRaises(errors.ClosureOrPrimopExpected,
                          stop_catch_interpretter, call(toy, func(["x"], "x")), env, store_)

        t_json = ["grab", "c", ["call", ["fun*", ["v"], ["call", "v", 10]], "c"]]
        parsed_json = parse(t_json)
        toy = receive(parsed_json)
        env, store_ = interpret_init()
        result, new_store = stop_catch_interpretter(call(toy, func(["x"], "x")), env, store_)
        self.assertEqual(result, 10)

        t_json = ["grab", "c", ["call", ["fun*", ["v"], ["call", "v", 10]], "c"]]
        parsed_json = parse(t_json)
        toy = receive(parsed_json)
        env, store_ = interpret_init()
        result, new_store = stop_catch_interpretter(call(toy, func(["x"], "x")), env, store_)
        self.assertEqual(result, 10)

        t_json = ["call", "+",
                  ["stop",
                   [["let", "y", "=", 10],
                    ["call", "^", 2, "y"]]],
                  10]
        parsed_json = parse(t_json)
        toy = receive(parsed_json)
        env, store_ = interpret_init()
        result, new_store = stop_catch_interpretter(call(toy, func(["x"], "x")), env, store_)
        self.assertEqual(result, 1024)

        t_json = ["call", "*",
                  ["call", ["fun*", [], 2]],
                  5]
        parsed_json = parse(t_json)
        toy = receive(parsed_json)
        env, store_ = interpret_init()
        result, new_store = stop_catch_interpretter(call(toy, func(["x"], "x")), env, store_)
        self.assertEqual(result, 10)

        t_json = ["call", ["fun*", [], 1]]
        parsed_json = parse(t_json)
        toy = receive(parsed_json)
        env, store_ = interpret_init()
        result, new_store = stop_catch_interpretter(call(toy, func(["x"], "x")), env, store_)
        self.assertEqual(result, 1)

        toy = func("k13", call(func("k", stop(func("kc", call("kc", 10)))),
                               func("of-1",
                                    call(func("k15", call("k15", 1)),
                                         func("of-0", call(func("k", call("k", ops_mapping["+"])),
                                                           func("k", call("k", ["k13", "of-0", "of-1"]))))))))
        env, store_ = interpret_init()
        result, new_store = stop_catch_interpretter(call(toy, func(["x"], "x")), env, store_)
        self.assertEqual(result, 10)

        toy = func(["kb"], declSequence([decl("x", func(["x", "f"], call("kb", "f"))),
                                         call(func("kc", call("kc", 10)),
                                              func("fa",
                                                   call(func("kd", call("kd", "x")),
                                                        func("fb", call("fb", ["kb", "fa"])))))]))
        env, store_ = interpret_init()
        result, new_store = stop_catch_interpretter(call(toy, func(["x"], "x")), env, store_)
        self.assertEqual(result, 10)

        toy = func("k13", call(func("k14", call("k14", 2)),
                               func("of-1",
                                    call(func("k15", call("k15", 1)),
                                         func("of-0", call(func("k", call("k", ops_mapping["+"])),
                                                           func("k", call("k", ["k13", "of-0", "of-1"]))))))))
        env, store_ = interpret_init()
        result, new_store = stop_catch_interpretter(call(toy, func(["x"], "x")), env, store_)
        self.assertEqual(result, 3)

    def test_seq(self):
        t_json_input = ["seq*", ["call", "+", ["call", "*", 5, 3], 1], -1]
        t_json_expected = call(func(["a"], -1), [call("+", [call("*", [5, 3]), 1])])
        self.assertTrue(alpha_equal(parse(t_json_input), t_json_expected))


def interpret_init():
    env = environment()
    s_store = store()
    for op in ops:
        env.pushTo(op[0], s_store.alloc())
        s_store.setAt(env.lookUp(op[0], s_store), op[1])
    return env, s_store


if __name__ == '__main__':
    unittest.main()
