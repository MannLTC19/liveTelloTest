#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <GL/glew.h>

#include <opencv2/opencv.hpp>
#include "System.h"

namespace py = pybind11;

class ORBSLAMRunner {
public:
    ORBSLAMRunner(const std::string& vocab,
                  const std::string& settings)
    {
        slam = new ORB_SLAM2::System(
            vocab,
            settings,
            ORB_SLAM2::System::MONOCULAR,
            true
        );
    }

    void process(py::array img, double timestamp)
    {
        py::buffer_info buf = img.request();

        if (buf.ndim != 2 && buf.ndim != 3) {
            throw std::runtime_error("Input image must be 2D (gray) or 3D (BGR)");
        }

        int height = buf.shape[0];
        int width  = buf.shape[1];
        int channels = (buf.ndim == 3) ? buf.shape[2] : 1;

        cv::Mat frame(
            height,
            width,
            (channels == 1) ? CV_8UC1 : CV_8UC3,
            buf.ptr
        );

        slam->TrackMonocular(frame, timestamp);
    }

    void shutdown()
    {
        slam->Shutdown();
    }

private:
    ORB_SLAM2::System* slam;
};

PYBIND11_MODULE(orbslam_runner, m)
{
    py::class_<ORBSLAMRunner>(m, "ORBSLAMRunner")
        .def(py::init<const std::string&, const std::string&>())
        .def("process", &ORBSLAMRunner::process)
        .def("shutdown", &ORBSLAMRunner::shutdown);
}
