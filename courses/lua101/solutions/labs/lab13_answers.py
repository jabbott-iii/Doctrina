# %% [markdown]
# # Lab 13: answer key
#
# Each tagged cell replaces the lab cell with the same tag; `tools/check_lab.py` runs the lab with
# them. The untagged Markdown cells explain the answers and the common mistakes.

# %% [markdown]
# ## Exercise L13.1
#
# Step 5, `insert -3`, moves the top value (the copied 1) to the position three from the top, which
# with four values is index 2. Step 6, `replace 1`, pops the top value, `'a'`, and stores it at
# index 1, overwriting the 1 there. Step 8, `remove -2`, removes the 2 under the `true`. Step 9,
# `settop 4`, grows the stack and fills the new place with `nil`. Common mistakes: reading `insert`
# as a copy (it moves the top value, so the stack keeps its size), and reading `replace` as
# keeping the top value in place.

# %% tags=["answer-L13.1"]
PREDICTION = [
    "1",
    "1 2",
    "1 2 'a'",
    "1 2 'a' 1",
    "1 1 2 'a'",
    "'a' 1 2",
    "'a' 1 2 true",
    "'a' 1 true",
    "'a' 1 true nil",
    "'a' 1",
]

# %% [markdown]
# ## Exercise L13.2
#
# `gcd` takes absolute values as unsigned integers, so that negating a negative number can't
# overflow, and runs Euclid's algorithm. `divmod` lets C divide, then corrects the result when the
# remainder and the divisor have different signs, which is when C's rounding toward zero and Lua's
# rounding down differ: `-7 / 2` is -3 remainder -1 in C, and `-7 // 2` is -4 remainder 1 in Lua.
#
# The key also handles `b == -1` on its own, because `math.mininteger / -1` overflows in C, which
# is undefined behavior and crashes many machines; Lua defines the result as `math.mininteger`
# again, with remainder 0. The lab's check leaves that case out. The one result the key can't
# give exactly is `gcd(math.mininteger, 0)`, whose true value, $2^{63}$, doesn't fit in a Lua
# integer and wraps to `math.mininteger`.
#
# Common mistakes: `luaL_checknumber` instead of `luaL_checkinteger`, which accepts 1.5 and
# truncates it silently; `return 1` after pushing two results, which drops `q`; and testing
# `b == 0` after dividing, which is too late.

# %% tags=["answer-L13.2"]
# %%writefile scratch/intmath.c
/* intmath: integer functions written in C. */
#include "lua.h"
#include "lauxlib.h"

/* gcd(a, b): the greatest common divisor of two integers, never negative. */
static int l_gcd(lua_State *L) {
  lua_Integer a = luaL_checkinteger(L, 1);
  lua_Integer b = luaL_checkinteger(L, 2);
  lua_Unsigned x = a < 0 ? 0u - (lua_Unsigned)a : (lua_Unsigned)a;
  lua_Unsigned y = b < 0 ? 0u - (lua_Unsigned)b : (lua_Unsigned)b;
  while (y != 0) {
    lua_Unsigned r = x % y;
    x = y;
    y = r;
  }
  lua_pushinteger(L, (lua_Integer)x);
  return 1;
}

/* divmod(a, b): a // b and a % b, rounded the way Lua rounds them. */
static int l_divmod(lua_State *L) {
  lua_Integer a = luaL_checkinteger(L, 1);
  lua_Integer b = luaL_checkinteger(L, 2);
  luaL_argcheck(L, b != 0, 2, "division by zero");
  if (b == -1) {                      /* a / -1 overflows for the smallest integer */
    lua_pushinteger(L, (lua_Integer)(0u - (lua_Unsigned)a));
    lua_pushinteger(L, 0);
    return 2;
  }
  lua_Integer q = a / b;              /* C rounds toward zero */
  lua_Integer r = a % b;
  if (r != 0 && (r < 0) != (b < 0)) { /* Lua rounds down: adjust when the signs differ */
    q -= 1;
    r += b;
  }
  lua_pushinteger(L, q);
  lua_pushinteger(L, r);
  return 2;
}

static const luaL_Reg functions[] = {
  { "gcd", l_gcd },
  { "divmod", l_divmod },
  { NULL, NULL },
};

int luaopen_intmath(lua_State *L) {
  luaL_newlib(L, functions);
  return 1;
}

# %% [markdown]
# ## Exercise L13.3
#
# Push the function and its argument, call it with one argument and one result, and on every path
# pop exactly the one value `lua_pcall` left: the result or the error message. Common mistakes:
# `lua_call`, which lets the error in `bad` reach the panic function and abort the program;
# forgetting the pop on one path, which the check with 150 words catches, since `stack:` then
# prints 50 or 100; and `lua_tointeger` without `lua_isinteger`, which turns 0.5 into 0 and
# reports a score.

# %% tags=["answer-L13.3"]
# %%writefile scratch/scorer.c
/* scorer: scores each word given on the command line with the function score in a Lua script. */
#include <stdio.h>
#include "lua.h"
#include "lauxlib.h"
#include "lualib.h"

/* Calls the script's score(word). On success, stores the result in *result and returns 1. On
   failure, prints "<word>: error: <message>" and returns 0. Either way, it leaves the stack as it
   found it. */
static int call_score(lua_State *L, const char *word, lua_Integer *result) {
  lua_getglobal(L, "score");
  lua_pushstring(L, word);
  if (lua_pcall(L, 1, 1, 0) != LUA_OK) {
    printf("%s: error: %s\n", word, lua_tostring(L, -1));
    lua_pop(L, 1);
    return 0;
  }
  if (!lua_isinteger(L, -1)) {
    printf("%s: error: score must return an integer\n", word);
    lua_pop(L, 1);
    return 0;
  }
  *result = lua_tointeger(L, -1);
  lua_pop(L, 1);
  return 1;
}

int main(int argc, char **argv) {
  if (argc < 2) {
    fprintf(stderr, "usage: scorer SCRIPT WORD...\n");
    return 2;
  }
  lua_State *L = luaL_newstate();
  luaL_openlibs(L);
  if (luaL_dofile(L, argv[1]) != LUA_OK) {
    fprintf(stderr, "scorer: %s\n", lua_tostring(L, -1));
    lua_close(L);
    return 1;
  }
  lua_Integer total = 0;
  for (int i = 2; i < argc; i++) {
    lua_Integer score;
    if (call_score(L, argv[i], &score)) {
      printf("%s: %lld\n", argv[i], (long long)score);
      total += score;
    }
  }
  printf("total: %lld\nstack: %d\n", (long long)total, lua_gettop(L));
  lua_close(L);
  return 0;
}

# %% [markdown]
# ## Exercise L13.4
#
# `bitset_new` initializes `words` to `NULL` and sets the metatable before it calls `calloc`, so
# that a failed allocation leaves a userdata whose `__gc` finds `NULL`. `set` returns the bitset by
# cutting the stack to its first argument, `lua_settop(L, 1)`. `__gc` frees only once, and counts
# only once, because it sets the pointer to `NULL`.
#
# A production type would also check for `NULL` in `check_bitset` and raise `bitset is freed`:
# after the check's explicit `__gc`, any method call on `keep` would read through a null pointer.
# Common mistakes: allocating with `malloc`, whose memory isn't zeroed, so bits start out set at
# random; `1 << p` instead of `1UL << p`, which shifts a 32-bit `int`, so the shift is undefined
# for positions 32 to 63 (compiled with gcc 13 on x86-64, setting bit 64 set 33 bits, from 32 to
# 64, and setting bit 40 set bit 8 instead); and decrementing `live` without the `NULL` test, which
# the second check catches.

# %% tags=["answer-L13.4"]
# %%writefile scratch/bitset.c
/* bitset: a fixed-size set of bits, held in memory that C allocates. */
#include <limits.h>
#include <stdlib.h>
#include "lua.h"
#include "lauxlib.h"

#define WORD_BITS (sizeof(unsigned long) * CHAR_BIT)

typedef struct {
  unsigned long *words; /* the bits, WORD_BITS to a word; NULL once freed */
  lua_Integer size;     /* the number of bits */
} Bitset;

static int live = 0; /* bitsets created and not yet freed */

static Bitset *check_bitset(lua_State *L) {
  return (Bitset *)luaL_checkudata(L, 1, "bitset");
}

/* The bit index at argument 2, checked to be from 1 to the bitset's size, counted from 0. */
static lua_Integer check_index(lua_State *L, Bitset *b) {
  lua_Integer i = luaL_checkinteger(L, 2);
  luaL_argcheck(L, 1 <= i && i <= b->size, 2, "index out of range");
  return i - 1;
}

/* bitset.new(size): a bitset of size bits, all clear. */
static int bitset_new(lua_State *L) {
  lua_Integer size = luaL_checkinteger(L, 1);
  luaL_argcheck(L, 1 <= size && size <= INT_MAX, 1, "size out of range");
  Bitset *b = (Bitset *)lua_newuserdatauv(L, sizeof(Bitset), 0);
  b->size = size;
  b->words = NULL;
  luaL_setmetatable(L, "bitset");
  b->words = calloc((size + WORD_BITS - 1) / WORD_BITS, sizeof(unsigned long));
  if (b->words == NULL) return luaL_error(L, "not enough memory");
  live++;
  return 1;
}

/* b:set(i): sets bit i; returns b. */
static int bitset_set(lua_State *L) {
  Bitset *b = check_bitset(L);
  lua_Integer i = check_index(L, b);
  b->words[i / WORD_BITS] |= 1UL << (i % WORD_BITS);
  lua_settop(L, 1);
  return 1;
}

/* b:test(i): true if bit i is set. */
static int bitset_test(lua_State *L) {
  Bitset *b = check_bitset(L);
  lua_Integer i = check_index(L, b);
  lua_pushboolean(L, (b->words[i / WORD_BITS] >> (i % WORD_BITS)) & 1UL);
  return 1;
}

/* b:count(): the number of bits set. */
static int bitset_count(lua_State *L) {
  Bitset *b = check_bitset(L);
  lua_Integer n = 0;
  for (lua_Integer i = 0; i < b->size; i++) n += (b->words[i / WORD_BITS] >> (i % WORD_BITS)) & 1UL;
  lua_pushinteger(L, n);
  return 1;
}

/* #b: the number of bits. */
static int bitset_len(lua_State *L) {
  lua_pushinteger(L, check_bitset(L)->size);
  return 1;
}

/* tostring(b): "bitset(<size>): <count> set". */
static int bitset_tostring(lua_State *L) {
  Bitset *b = check_bitset(L);
  bitset_count(L);
  lua_pushfstring(L, "bitset(%I): %I set", (LUAI_UACINT)b->size, (LUAI_UACINT)lua_tointeger(L, -1));
  return 1;
}

/* Frees the bits, once: the collector, or a program, may call __gc again. */
static int bitset_gc(lua_State *L) {
  Bitset *b = check_bitset(L);
  if (b->words != NULL) {
    free(b->words);
    b->words = NULL;
    live--;
  }
  return 0;
}

/* bitset.live(): the number of bitsets not yet freed. */
static int bitset_live(lua_State *L) {
  lua_pushinteger(L, live);
  return 1;
}

static const luaL_Reg methods[] = {
  { "set", bitset_set },
  { "test", bitset_test },
  { "count", bitset_count },
  { "__len", bitset_len },
  { "__tostring", bitset_tostring },
  { "__gc", bitset_gc },
  { NULL, NULL },
};

static const luaL_Reg functions[] = {
  { "new", bitset_new },
  { "live", bitset_live },
  { NULL, NULL },
};

int luaopen_bitset(lua_State *L) {
  luaL_newmetatable(L, "bitset");
  luaL_setfuncs(L, methods, 0);
  lua_pushvalue(L, -1);
  lua_setfield(L, -2, "__index");
  luaL_newlib(L, functions);
  return 1;
}
