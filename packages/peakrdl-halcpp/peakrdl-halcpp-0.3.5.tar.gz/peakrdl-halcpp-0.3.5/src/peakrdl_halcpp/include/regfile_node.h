#ifndef _REGFILE_NODE_H_
#define _REGFILE_NODE_H_

#include "arch_io.h"
#include <cstdint>

namespace halcpp{

template <uint32_t BASE, typename PARENT_TYPE>
class RegfileNode {
public:
    static constexpr uint32_t get_abs_addr() { return PARENT_TYPE().get_abs_addr() + BASE; }

    static inline uint32_t get(const uint32_t addr) { return PARENT_TYPE::get(addr + BASE); }
    static inline void set(const uint32_t addr, uint32_t val) {
        PARENT_TYPE::set(addr + BASE, val);
    }
};

};

#endif // !_REGFILE_NODE_H_

