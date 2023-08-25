// Copyright (C) 2004-2021 Artifex Software, Inc.
//
// This file is part of MuPDF.
//
// MuPDF is free software: you can redistribute it and/or modify it under the
// terms of the GNU Affero General Public License as published by the Free
// Software Foundation, either version 3 of the License, or (at your option)
// any later version.
//
// MuPDF is distributed in the hope that it will be useful, but WITHOUT ANY
// WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
// details.
//
// You should have received a copy of the GNU Affero General Public License
// along with MuPDF. If not, see <https://www.gnu.org/licenses/agpl-3.0.en.html>
//
// Alternative licensing terms are available from the licensor.
// For commercial licensing, see <https://www.artifex.com/> or contact
// Artifex Software, Inc., 1305 Grant Avenue - Suite 200, Novato,
// CA 94945, U.S.A., +1(415)492-9861, for further information.

#ifndef FZ_CONFIG_H

#define FZ_CONFIG_H

/**
	Enable the following for spot (and hence overprint/overprint
	simulation) capable rendering. This forces FZ_PLOTTERS_N on.
*/
/* #define FZ_ENABLE_SPOT_RENDERING 1 */

/**
	Choose which plotters we need.
	By default we build all the plotters in. To avoid building
	plotters in that aren't needed, define the unwanted
	FZ_PLOTTERS_... define to 0.
*/
/* #define FZ_PLOTTERS_G 1 */
/* #define FZ_PLOTTERS_RGB 1 */
/* #define FZ_PLOTTERS_CMYK 1 */
/* #define FZ_PLOTTERS_N 1 */

/**
	Choose which document agents to include.
	By default all are enabled. To avoid building unwanted
	ones, define FZ_ENABLE_... to 0.
*/
/* #define FZ_ENABLE_PDF 1 */
/* #define FZ_ENABLE_XPS 1 */
/* #define FZ_ENABLE_SVG 1 */
/* #define FZ_ENABLE_CBZ 1 */
/* #define FZ_ENABLE_IMG 1 */
/* #define FZ_ENABLE_HTML 1 */
/* #define FZ_ENABLE_EPUB 1 */

/**
	Choose which document writers to include.
	By default all are enabled. To avoid building unwanted
	ones, define FZ_ENABLE_..._OUTPUT to 0.
*/
/* #define FZ_ENABLE_OCR_OUTPUT 1 */
/* #define FZ_ENABLE_DOCX_OUTPUT 1 */
/* #define FZ_ENABLE_ODT_OUTPUT 1 */

/**
	Choose whether to enable ICC color profiles.
*/
/* #define FZ_ENABLE_ICC 1 */

/**
	Choose whether to enable JPEG2000 decoding.
	By default, it is enabled, but due to frequent security
	issues with the third party libraries we support disabling
	it with this flag.
*/
/* #define FZ_ENABLE_JPX 1 */

/**
	Choose whether to enable JavaScript.
	By default JavaScript is enabled both for mutool and PDF
	interactivity.
*/
/* #define FZ_ENABLE_JS 1 */

/**
	Choose which fonts to include.
	By default we include the base 14 PDF fonts,
	DroidSansFallback from Android for CJK, and
	Charis SIL from SIL for epub/html.
	Enable the following defines to AVOID including
	unwanted fonts.
*/
/* To avoid all noto fonts except CJK, enable: */
/* #define TOFU */

/* To skip the CJK font, enable: (this implicitly enables TOFU_CJK_EXT
 * and TOFU_CJK_LANG) */
/* #define TOFU_CJK */

/* To skip CJK Extension A, enable: (this implicitly enables
 * TOFU_CJK_LANG) */
#define TOFU_CJK_EXT 1

/* To skip CJK language specific fonts, enable: */
/* #define TOFU_CJK_LANG */

/* To skip the Emoji font, enable: */
/* #define TOFU_EMOJI */

/* To skip the ancient/historic scripts, enable: */
/* #define TOFU_HISTORIC */

/* To skip the symbol font, enable: */
/* #define TOFU_SYMBOL */

/* To skip the SIL fonts, enable: */
/* #define TOFU_SIL */

/* To skip the Base14 fonts, enable: */
/* #define TOFU_BASE14 */
/* (You probably really don't want to do that except for measurement
 * purposes!) */

/* ---------- DO NOT EDIT ANYTHING UNDER THIS LINE ---------- */

#ifndef FZ_ENABLE_SPOT_RENDERING
#define FZ_ENABLE_SPOT_RENDERING 1
#endif

#if FZ_ENABLE_SPOT_RENDERING
#undef FZ_PLOTTERS_N
#define FZ_PLOTTERS_N 1
#endif /* FZ_ENABLE_SPOT_RENDERING */

#ifndef FZ_PLOTTERS_G
#define FZ_PLOTTERS_G 1
#endif /* FZ_PLOTTERS_G */

#ifndef FZ_PLOTTERS_RGB
#define FZ_PLOTTERS_RGB 1
#endif /* FZ_PLOTTERS_RGB */

#ifndef FZ_PLOTTERS_CMYK
#define FZ_PLOTTERS_CMYK 1
#endif /* FZ_PLOTTERS_CMYK */

#ifndef FZ_PLOTTERS_N
#define FZ_PLOTTERS_N 1
#endif /* FZ_PLOTTERS_N */

/* We need at least 1 plotter defined */
#if FZ_PLOTTERS_G == 0 && FZ_PLOTTERS_RGB == 0 && FZ_PLOTTERS_CMYK == 0
#undef FZ_PLOTTERS_N
#define FZ_PLOTTERS_N 1
#endif

#ifndef FZ_ENABLE_PDF
#define FZ_ENABLE_PDF 1
#endif /* FZ_ENABLE_PDF */

#ifndef FZ_ENABLE_XPS
#define FZ_ENABLE_XPS 1
#endif /* FZ_ENABLE_XPS */

#ifndef FZ_ENABLE_SVG
#define FZ_ENABLE_SVG 1
#endif /* FZ_ENABLE_SVG */

#ifndef FZ_ENABLE_CBZ
#define FZ_ENABLE_CBZ 1
#endif /* FZ_ENABLE_CBZ */

#ifndef FZ_ENABLE_IMG
#define FZ_ENABLE_IMG 1
#endif /* FZ_ENABLE_IMG */

#ifndef FZ_ENABLE_HTML
#define FZ_ENABLE_HTML 1
#endif /* FZ_ENABLE_HTML */

#ifndef FZ_ENABLE_EPUB
#define FZ_ENABLE_EPUB 1
#endif /* FZ_ENABLE_EPUB */

#ifndef FZ_ENABLE_OCR_OUTPUT
#define FZ_ENABLE_OCR_OUTPUT 1
#endif /* FZ_ENABLE_OCR_OUTPUT */

#ifndef FZ_ENABLE_ODT_OUTPUT
#define FZ_ENABLE_ODT_OUTPUT 1
#endif /* FZ_ENABLE_ODT_OUTPUT */

#ifndef FZ_ENABLE_DOCX_OUTPUT
#define FZ_ENABLE_DOCX_OUTPUT 1
#endif /* FZ_ENABLE_DOCX_OUTPUT */

#ifndef FZ_ENABLE_JPX
#define FZ_ENABLE_JPX 1
#endif /* FZ_ENABLE_JPX */

#ifndef FZ_ENABLE_JS
#define FZ_ENABLE_JS 1
#endif /* FZ_ENABLE_JS */

#ifndef FZ_ENABLE_ICC
#define FZ_ENABLE_ICC 1
#endif /* FZ_ENABLE_ICC */

/* If Epub and HTML are both disabled, disable SIL fonts */
#if FZ_ENABLE_HTML == 0 && FZ_ENABLE_EPUB == 0
#undef TOFU_SIL
#define TOFU_SIL
#endif

#if !defined(HAVE_LEPTONICA) || !defined(HAVE_TESSERACT)
#ifndef OCR_DISABLED
#define OCR_DISABLED
#endif
#endif

#endif /* FZ_CONFIG_H */
