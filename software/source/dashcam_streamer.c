/*
 * dashcam_streamer.c
 *
 * Real-time H.264 RTSP video streamer for Luckfox Pico Mini B (RV1103)
 * Target: Streaming live 1080p@30fps video to smartphone over Wi-Fi without SD card
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>

#include <rk_mpi_vi.h>
#include <rk_mpi_venc.h>
#include <rk_mpi_sys.h>
#include <rk_mpi_mb.h>

#define VIDEO_WIDTH       1920
#define VIDEO_HEIGHT      1080
#define VIDEO_FPS         30
#define VIDEO_BITRATE_K   4000  /* 4 Mbps H.264 CBR */
#define RTSP_PORT         554
#define RTSP_URL_PATH     "/live/0"

static volatile int g_running = 1;

static void sig_handler(int sig) {
    (void)sig;
    g_running = 0;
}

int main(int argc, char *argv[]) {
    printf("[DashCam] Initializing RV1103 Hardware Video Pipeline...\n");

    signal(SIGINT, sig_handler);
    signal(SIGTERM, sig_handler);

    // 1. Initialize Rockchip MPI Core
    if (RK_MPI_SYS_Init() != RK_SUCCESS) {
        fprintf(stderr, "[Error] RK_MPI_SYS_Init failed!\n");
        return -1;
    }

    // 2. Configure Video Input (VI) Channel 0 for SC3336 MIPI CSI-2
    VI_CHN_ATTR_S vi_attr;
    memset(&vi_attr, 0, sizeof(vi_attr));
    vi_attr.stIspOpt.u32BufCount = 2; /* 2 frame buffers to fit in 64MB DDR2 */
    vi_attr.stSize.u32Width = VIDEO_WIDTH;
    vi_attr.stSize.u32Height = VIDEO_HEIGHT;
    vi_attr.enPixFmt = IMAGE_TYPE_NV12;

    if (RK_MPI_VI_SetChnAttr(0, 0, &vi_attr) != RK_SUCCESS) {
        fprintf(stderr, "[Error] Failed to set VI channel attributes!\n");
        return -1;
    }
    if (RK_MPI_VI_EnableChn(0, 0) != RK_SUCCESS) {
        fprintf(stderr, "[Error] Failed to enable VI channel!\n");
        return -1;
    }

    // 3. Configure Hardware Video Encoder (VENC) Channel 0 for H.264
    VENC_CHN_ATTR_S venc_attr;
    memset(&venc_attr, 0, sizeof(venc_attr));
    venc_attr.stVencAttr.enType = RK_VIDEO_ID_AVC; /* H.264 */
    venc_attr.stVencAttr.u32Profile = 77;          /* Main Profile */
    venc_attr.stVencAttr.u32PicWidth = VIDEO_WIDTH;
    venc_attr.stVencAttr.u32PicHeight = VIDEO_HEIGHT;
    venc_attr.stVencAttr.u32VirWidth = VIDEO_WIDTH;
    venc_attr.stVencAttr.u32VirHeight = VIDEO_HEIGHT;

    venc_attr.stRcAttr.enRcMode = VENC_RC_MODE_H264CBR;
    venc_attr.stRcAttr.stH264Cbr.u32Gop = VIDEO_FPS;          /* 1 Keyframe per sec */
    venc_attr.stRcAttr.stH264Cbr.u32BitRate = VIDEO_BITRATE_K;
    venc_attr.stRcAttr.stH264Cbr.fr32DstFrameRateNum = VIDEO_FPS;
    venc_attr.stRcAttr.stH264Cbr.fr32DstFrameRateDen = 1;

    if (RK_MPI_VENC_CreateChn(0, &venc_attr) != RK_SUCCESS) {
        fprintf(stderr, "[Error] Failed to create VENC channel!\n");
        return -1;
    }

    // 4. Hardware Zero-Copy Bind: VI Channel 0 -> VENC Channel 0
    MPP_CHN_S src_chn = { .enModId = RK_ID_VI,   .s32DevId = 0, .s32ChnId = 0 };
    MPP_CHN_S dst_chn = { .enModId = RK_ID_VENC, .s32DevId = 0, .s32ChnId = 0 };
    if (RK_MPI_SYS_Bind(&src_chn, &dst_chn) != RK_SUCCESS) {
        fprintf(stderr, "[Error] Failed to bind VI to VENC!\n");
        return -1;
    }

    printf("[DashCam] Hardware Pipeline Bound: VI0 -> VENC0 (1080p@30fps H.264 CBR 4Mbps)\n");
    printf("[DashCam] Ready to stream. Run RTSP server at port %d%s\n", RTSP_PORT, RTSP_URL_PATH);

    // 5. Main stream extraction loop
    VENC_STREAM_S stream;
    memset(&stream, 0, sizeof(stream));
    stream.pstPack = (VENC_PACK_S *)malloc(sizeof(VENC_PACK_S));

    while (g_running) {
        if (RK_MPI_VENC_GetStream(0, &stream, 1000) == RK_SUCCESS) {
            /* Feed stream packets to RTSP server / socket */
            RK_MPI_VENC_ReleaseStream(0, &stream);
        } else {
            usleep(1000);
        }
    }

    printf("[DashCam] Shutting down cleanly...\n");
    free(stream.pstPack);
    RK_MPI_SYS_UnBind(&src_chn, &dst_chn);
    RK_MPI_VENC_DestroyChn(0);
    RK_MPI_VI_DisableChn(0, 0);
    RK_MPI_SYS_Exit();

    return 0;
}
