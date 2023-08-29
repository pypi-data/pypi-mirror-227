#ifndef _ARRAY_NODES_H__
#define _ARRAY_NODES_H__

#include <type_traits>
#include <cstdint>
#include <utility>
#include <array>
#include "halcpp_utils.h"

namespace halcpp{
// Credit for this solution goes to https://www.reddit.com/user/IyeOnline/

template<int32_t INDEX, uint32_t DIM>
constexpr uint32_t map_index()
{
    return INDEX == -1 ? DIM-1 : INDEX;
}

template<uint32_t STRIDE, std::size_t N>
constexpr uint32_t linear_index( std::array<uint32_t,N> nd_index, std::array<uint32_t,N> dimensions )
{
    uint32_t result = 0;
    uint32_t product = 1;
    for ( std::size_t i=0; i<N; ++i )
    {
        result += nd_index[N-i-1] * STRIDE * product;
        product *= dimensions[N-i-1];
    }

    return result;
}

constexpr bool valid_index( int32_t I, uint32_t E )
{
    return  I >= -1 and I < static_cast<int32_t>(E);
}

template< 
    template<uint32_t B, uint32_t W, typename P> typename REG_T,
    uint32_t BASE, uint32_t WIDTH, uint32_t STRIDE, typename PARENT_TYPE, uint32_t ... Extents
>
class  RegArrayNode
{
private:
    static constexpr uint32_t Dimensions = sizeof...(Extents);
    static_assert( Dimensions > 0 );
public :
    static constexpr uint32_t stride = STRIDE;
    static_assert( Dimensions > 0 );

    template<int32_t ... Indices>
    auto at()
    {
        static_assert( sizeof...(Indices) == Dimensions );
        static_assert( ( valid_index(Indices,Extents) && ... ) );
        constexpr uint32_t offset = BASE + linear_index<STRIDE>( std::array{ map_index<Indices,Extents>() ... }, std::array{ Extents ... } );

        return REG_T< offset, WIDTH, PARENT_TYPE >();
    }

    template<uint32_t IDX>
    constexpr uint32_t get_dim(){
        static_assert(IDX < Dimensions, "Index out of bounds");

        constexpr std::array<uint32_t, Dimensions> dimensions_array = {Extents...};
        return dimensions_array[IDX];
    }
};

template< 
    template<uint32_t B, typename P> typename REGFILE_T,
    uint32_t BASE, uint32_t STRIDE, typename PARENT_TYPE, uint32_t ... Extents
>
class RegfileArrayNode
{
private:
    static constexpr uint32_t Dimensions = sizeof...(Extents);
    static_assert( Dimensions > 0 );
public :
    static constexpr uint32_t stride = STRIDE;

    template<int32_t ... Indices>
    auto at()
    {
        static_assert( sizeof...(Indices) == Dimensions );
        static_assert( ( valid_index(Indices,Extents) && ... ) );
        constexpr uint32_t offset = BASE + linear_index<STRIDE>( std::array{ map_index<Indices,Extents>() ... }, std::array{ Extents ... } );

        return REGFILE_T< offset, PARENT_TYPE >();
    }

    template<uint32_t IDX>
    constexpr uint32_t get_dim(){
        static_assert(IDX < Dimensions, "Index out of bounds");

        constexpr std::array<uint32_t, Dimensions> dimensions_array = {Extents...};
        return dimensions_array[IDX];
    }
};

namespace __halcpp_utils {

template<class T, T... inds, class F>
constexpr void loop(std::integer_sequence<T, inds...>, F&& f) {
    (f(std::integral_constant<T, inds>{}), ...);
}
}

template<class T, T count, class F>
constexpr void loop(F&& f) {
    __halcpp_utils::loop(std::make_integer_sequence<T, count>{}, std::forward<F>(f));
}

}

#endif // !_ARRAY_NODES_H__


