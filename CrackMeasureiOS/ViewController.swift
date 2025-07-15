import UIKit
import RealityKit
import ARKit

class ViewController: UIViewController {
    @IBOutlet var arView: ARView!
    var points: [SIMD3<Float>] = []

    override func viewDidLoad() {
        super.viewDidLoad()

        let config = ARWorldTrackingConfiguration()
        config.planeDetection = [.horizontal, .vertical]
        arView.session.run(config)

        let tapGesture = UITapGestureRecognizer(target: self, action: #selector(handleTap(_:)))
        arView.addGestureRecognizer(tapGesture)
    }

    @objc func handleTap(_ sender: UITapGestureRecognizer) {
        let location = sender.location(in: arView)
        let results = arView.raycast(from: location, allowing: .estimatedPlane, alignment: .any)
        if let firstResult = results.first {
            let position = firstResult.worldTransform.translation
            points.append(position)

            if points.count == 2 {
                let distance = simd_distance(points[0], points[1])
                let distanceInMM = distance * 1000
                print("距離: \(distanceInMM) mm")
                points.removeAll()
            }
        }
    }
}

extension matrix_float4x4 {
    var translation: SIMD3<Float> {
        return [columns.3.x, columns.3.y, columns.3.z]
    }
}
