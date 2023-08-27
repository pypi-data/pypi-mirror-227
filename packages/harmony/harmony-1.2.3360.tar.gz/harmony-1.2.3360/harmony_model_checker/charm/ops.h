#ifndef SRC_OPS_H
#define SRC_OPS_H

#include <inttypes.h>

#include "charm.h"
#include "value.h"
#include "global.h"

#define MAX_PRINT       64
#define MAX_ARGS         8

void ops_init(struct global *global, struct engine *engine);
struct op_info *ops_get(char *opname, int size);

// This contains information that is kept when the execution of some thread
// is evaluated from some state.  During re-execution when a counter-example
// is re-evaluated, more information is kept.
struct step {
    struct engine engine;           // allocator and global variabels
    struct context *ctx;            // points to the context (state of the thread)
    struct access_info *ai;         // info about load and store operations

    // TODO This field is a bit of a misnomer.  It is set during re-execution
    // of a counter-example and instructs the Harmony instructions to keep
    // additional information.  In particular this includes the callstack.
    bool keep_callstack;

    // The extra information that is kept
    struct strbuf explain;              // human-readable explanation of step
    hvalue_t explain_args[MAX_ARGS];    // arguments to the explanation
    unsigned int explain_nargs;         // #arguments
    struct callstack *callstack;        // call stack (method invocations)
    unsigned int nlog;                  // output values that are printed
    hvalue_t log[MAX_PRINT];            // #output values
};

// Information about a Harmony instruction.  For each there are three methods:
//      - initialize and return specific arnuments
//      - execute the instruction
//      - print what an execution is about to do (without doing it)
struct op_info {
    const char *name;       // name of the instruction
    void *(*init)(struct dict *, struct engine *engine);
    void (*op)(const void *env, struct state *state, struct step *step, struct global *global);
    void (*next)(const void *env, struct context *ctx, struct global *global, FILE *fp);
};

// Each instruction can have one or more arguments in the code.  Which arguments
// depends on the instruction.  They are described below.

struct env_Apply {
    hvalue_t method;
};

struct env_Builtin {
    hvalue_t method;
};

struct env_Cut {
    struct var_tree *key, *value;
};

struct env_Del {
    hvalue_t *indices;
    unsigned int n;
};

struct env_DelVar {
    hvalue_t name;
};

struct env_Frame {
    hvalue_t name;
    struct var_tree *args;
};

struct env_AtomicInc {
    bool lazy;
};

struct env_Finally {
    unsigned int pc;
};

struct env_Invariant {
    unsigned int pc;
    bool pre;
};

struct env_Jump {
    unsigned int pc;
};

struct env_JumpCond {
    hvalue_t cond;
    unsigned int pc;
};

struct env_Load {
    hvalue_t *indices;
    unsigned int n;
};

struct env_LoadVar {
    hvalue_t name;
};

struct env_Move {
    int offset;
};

struct env_Nary {
    unsigned int arity;
    struct f_info *fi;
};

struct env_Push {
    hvalue_t value;
};

struct env_Return {
    hvalue_t result;      // may be 0
    hvalue_t deflt;       // may be 0
};

struct env_Spawn {
    bool eternal;
};

struct env_Split {
    unsigned int count;
};

struct env_Stop {
    hvalue_t *indices;
    unsigned int n;
};

struct env_Store {
    hvalue_t *indices;
    unsigned int n;
    hvalue_t address;
};

struct env_StoreVar {
    struct var_tree *args;
};

void interrupt_invoke(struct step *step);

#endif //SRC_OPS_H
