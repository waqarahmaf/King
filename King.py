cmake_minimum_required(VERSION 2.8)

project(unicodeHelper)

cmake_policy(SET CMP0046 OLD)

option(UNICODE_HELPER_USE_CP932 "CP932(MS-SJIS)用関数を用意" ON)

#  unicode.orgにあるコード<->unicodeの定義TXTをcのテーブルとして出力するツール
add_executable(convunicodeorg
  ${CMAKE_CURRENT_SOURCE_DIR}/tools/convunicodeorg.cpp
  )


#  optionalな変換要テーブルの作成ターゲット
add_custom_target(unicodeHelperOptional)

#  cp932(microsoft拡張sjis)のテーブル作成ルール
if(UNICODE_HELPER_USE_CP932)
  set(UNICODE_HELPER_CP932_SOURCE "${CMAKE_CURRENT_BINARY_DIR}/cp932.inc")

  file(DOWNLOAD
	http://unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WINDOWS/CP932.TXT
	${CMAKE_CURRENT_BINARY_DIR}/CP932.TXT
	)

  add_custom_command(
	COMMAND convunicodeorg
	ARGS    ${CMAKE_CURRENT_BINARY_DIR}/CP932.TXT
	        ${UNICODE_HELPER_CP932_SOURCE}
			cp932
	TARGET	unicodeHelperOptional
	OUTPUTS ${UNICODE_HELPER_CP932_SOURCE}
	DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/CP932.TXT
	)

endif()

set(SRCDIR ${CMAKE_CURRENT_SOURCE_DIR}/srcs)
set(INCDIR ${CMAKE_CURRENT_SOURCE_DIR}/srcs)

#  optionの結果をbuildに反映させるためのconfigヘッダ
configure_file(
  ${SRCDIR}/text/unicodeHelperConfig.h.in
  ${CMAKE_CURRENT_BINARY_DIR}/text/unicodeHelperConfig.h
  )

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/srcs ${CMAKE_CURRENT_BINARY_DIR})

#  UnicodeHelperのルール
add_library(unicodeHelper STATIC
  ${SRCDIR}/text/unicodeHelper.cpp
  )

add_dependencies(unicodeHelper
  unicodeHelperOptional
  )

install(TARGETS unicodeHelper DESTINATION lib)
install(FILES
  ${SRCDIR}/text/unicodeHelper.h DESTINATION include/text
  )
