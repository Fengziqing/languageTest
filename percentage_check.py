import get_diff
import classify_and_check
#全局百分号核对
if __name__ == '__main__':
    """
        check_url:本机需要核对多语言上级目录
            mac client:
            /Users/haru.feng/Documents/SourceCode/release-client-5.15.x/mac-client/Zoom/Zoom/Zoom
            /Users/haru.feng/Documents/SourceCode/ep-new-release/mac-client/Zoom/Zoom/Zoom
            clips:
            /Users/haru.feng/Documents/SourceCode/release-client-5.15.x/mac-client/ZoomClips/ZoomClips/ZoomClips/SupportingFiles
            /Users/haru.feng/Documents/SourceCode/ep-new-release/mac-client/ZoomClips/ZoomClips/ZoomClips/SupportingFiles
    """
    check_url = '/Users/haru.feng/Documents/SourceCode/release-client-5.15.x/mac-client/ZoomClips/ZoomClips/ZoomClips/SupportingFiles'
    classified_array = classify_and_check.filter_string_with_path(check_url)
    classify_and_check.makeKeyAndValue_and_check(classified_array)