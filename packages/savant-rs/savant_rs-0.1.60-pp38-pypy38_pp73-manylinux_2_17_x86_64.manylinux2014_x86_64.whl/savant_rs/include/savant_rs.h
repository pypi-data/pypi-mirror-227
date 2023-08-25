#include <stdarg.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>

/**
 * # Safety
 *
 * The function is intended for invocation from C/C++, so it is unsafe by design.
 */
bool check_version(const char *external_version);

/**
 * # Safety
 *
 * The function is intended for invocation from C/C++, so it is unsafe by design.
 */
void pipeline2_move_as_is(uintptr_t handle,
                          const char *dest_stage,
                          const int64_t *ids,
                          uintptr_t len);

/**
 * # Safety
 *
 * The function is intended for invocation from C/C++, so it is unsafe by design.
 */
int64_t pipeline2_move_and_pack_frames(uintptr_t handle,
                                       const char *dest_stage,
                                       const int64_t *frame_ids,
                                       uintptr_t len);

/**
 * # Safety
 *
 * The function is intended for invocation from C/C++, so it is unsafe by design.
 */
uintptr_t pipeline2_move_and_unpack_batch(uintptr_t handle,
                                          const char *dest_stage,
                                          int64_t batch_id,
                                          int64_t *resulting_ids,
                                          uintptr_t resulting_ids_len);
