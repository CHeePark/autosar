/**
 * @file tpl_app_config.h
 *
 * @section desc File description
 *
 * Header of the automatic generated constants usable
 * by the application BCM_SYSTEM
 * Automatically generated by goil on Www Mmm dd hh:mm:ss yyyy
 * from root OIL file main_bcm.oil
 *
 * @section copyright Copyright
 *
 * Trampoline OS
 *
 * Trampoline is copyright (c) IRCCyN 2005-2007
 * Trampoline is protected by the French intellectual property law.
 *
 * This software is distributed under the Lesser GNU Public Licence
 *
 * @section infos File informations
 *
 * $Date$
 * $Rev$
 * $Author$
 * $URL$
 */

#ifndef TPL_APP_CONFIG_H
#define TPL_APP_CONFIG_H

#include "tpl_app_define.h"
#include "tpl_compiler.h"

/*=============================================================================
 * proc_name_table is an array of strings containing the name of the
 * processes. It may be used by the application for debugging purpose
 */
#if !defined(NO_TASK) || !defined(NO_ISR)
#define API_START_SEC_CONST_UNSPECIFIED
#include "tpl_memmap.h"
extern CONSTP2CONST(char, AUTOMATIC, OS_APPL_DATA)
  proc_name_table[TASK_COUNT + ISR_COUNT + 1];
#define API_STOP_SEC_CONST_UNSPECIFIED
#include "tpl_memmap.h"
#endif

/*=============================================================================
 * Declaration of Counters constants
 */

/*=============================================================================
 * Declaration of flags macros
 */

#endif

/* End of file TPL_APP_CONFIG_H */

